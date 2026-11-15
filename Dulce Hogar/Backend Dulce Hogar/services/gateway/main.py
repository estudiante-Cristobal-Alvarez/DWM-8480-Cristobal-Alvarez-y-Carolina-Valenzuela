import os
from typing import List, Optional
import strawberry
import httpx
import jwt

from strawberry.types import Info
from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from strawberry.extensions import QueryDepthLimiter
from strawberry.extensions import AddValidationRules
from services.gateway.graphql_limits import MaxFieldsRule


ORDERS_URL = os.getenv("ORDERS_URL", "http://127.0.0.1:9002")

ORDERS_INTERNAL_SECRET = os.getenv("ORDERS_INTERNAL_SECRET")

INVENTORY_URL = os.getenv("INVENTORY_URL", "http://127.0.0.1:9001")

CLIENTS_URL = os.getenv("CLIENTS_URL", "http://127.0.0.1:9003")

CLIENTS_INTERNAL_SECRET = os.getenv("CLIENTS_INTERNAL_SECRET")

# Configuración de HashiCorp Vault
VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")

VAULT_TOKEN = os.getenv("VAULT_TOKEN")

# Configuración JWT
JWT_ALGORITHM = "HS256"

def obtener_clave_jwt():
    if not VAULT_TOKEN:
        raise RuntimeError(
            "El token de Vault no está configurado"
        )

    try:
        respuesta = httpx.get(
            f"{VAULT_ADDR}/v1/secret/data/auth",
            headers={"X-Vault-Token": VAULT_TOKEN},
            timeout=5.0
        )

        respuesta.raise_for_status()

        datos = respuesta.json()
        clave_jwt = datos["data"]["data"]["jwt_secret_key"]

        if not clave_jwt:
            raise ValueError("La clave JWT está vacía")

        return clave_jwt

    except (httpx.HTTPError, KeyError, ValueError) as error:
        raise RuntimeError(
            "No se pudo obtener la clave JWT desde Vault"
        ) from error

def validar_token_jwt(token: str) -> dict:
    try:
        clave_jwt = obtener_clave_jwt()

        datos = jwt.decode(
            token,
            clave_jwt,
            algorithms=[JWT_ALGORITHM],
            options={"require": ["sub", "exp", "iat"]}
        )

        return datos

    except jwt.ExpiredSignatureError as error:
        raise ValueError(
            "El token JWT ha expirado"
        ) from error

    except jwt.InvalidTokenError as error:
        raise ValueError(
            "El token JWT no es válido"
        ) from error

async def obtener_contexto(request: Request) -> dict:
    autorizacion = request.headers.get("Authorization", "")

    if not autorizacion.startswith("Bearer "):
        return {
            "usuario": None,
            "error_autenticacion": "Se requiere un token Bearer"
        }

    token = autorizacion[7:].strip()

    if not token:
        return {
            "usuario": None,
            "error_autenticacion": "El token JWT está vacío"
        }

    try:
        datos_usuario = validar_token_jwt(token)

        return {
            "usuario": datos_usuario,
            "error_autenticacion": None
        }

    except ValueError as error:
        return {
            "usuario": None,
            "error_autenticacion": str(error)
        }

# Tipos GraphQL

@strawberry.type
class DetallePedidoType:
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float


@strawberry.type
class ProductoType:
    id: int
    nombre: str
    categoria: str
    precio: float
    disponible: bool


@strawberry.type
class PedidoType:
    id: int
    cliente_id: int
    estado: str
    total: float
    metodo_pago: str
    estado_pago: str
    codigo_transaccion: Optional[str]
    detalles: List[DetallePedidoType]

@strawberry.type
class ProductoResumenType:
    producto_id: int
    nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float


@strawberry.type
class ResumenPedidoType:
    id: int
    cliente_id: int
    estado: str
    total: float
    metodo_pago: str
    estado_pago: str
    codigo_transaccion: Optional[str]
    productos: List[ProductoResumenType]

# Consultas GraphQL

# Función auxiliar para consultar pedidos autorizados
async def obtener_pedido_autorizado(
    info: Info,
    order_id: int
) -> Optional[PedidoType]:

    # Verificar autenticación JWT
    usuario = info.context.get("usuario")

    if usuario is None:
        mensaje = info.context.get(
            "error_autenticacion",
            "No autenticado"
        )
        raise ValueError(
            f"Acceso denegado: {mensaje}"
        )

    # Verificar que la clave interna esté configurada
    if not ORDERS_INTERNAL_SECRET:
        raise ValueError(
            "La seguridad interna de Orders no está configurada"
        )

    # Consultar Orders Service
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{ORDERS_URL}/orders/{order_id}",
                headers={
                    "X-Orders-Secret": ORDERS_INTERNAL_SECRET
                }
            )
    except httpx.RequestError:
        raise ValueError(
            "Orders Service no está disponible"
        )

    if response.status_code == 404:
        return None

    if response.status_code != 200:
        raise ValueError(
            "Error al consultar Orders Service"
        )

    data = response.json()

    # Verificar que el pedido pertenece al usuario autenticado
    correo_usuario = usuario.get("correo")

    if not correo_usuario:
        raise ValueError(
            "Acceso denegado: El JWT no contiene el correo del usuario"
        )

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            respuesta_cliente = await client.get(
                f"{CLIENTS_URL}/clients/{data['cliente_id']}",
                headers={
                    "X-Clients-Secret": CLIENTS_INTERNAL_SECRET or ""
                }
            )

    except httpx.RequestError:
        raise ValueError(
            "Clients Service no está disponible"
        )

    if respuesta_cliente.status_code == 404:
        raise ValueError(
            "Acceso denegado: No se pudo verificar el propietario del pedido"
        )

    if respuesta_cliente.status_code != 200:
        raise ValueError(
            "Error al consultar Clients Service"
        )

    cliente = respuesta_cliente.json()

    if (
        cliente["correo"].strip().casefold()
        != correo_usuario.strip().casefold()
    ):
        raise ValueError(
            "Acceso denegado: El pedido no pertenece al usuario autenticado"
        )

    detalles = [
        DetallePedidoType(**detalle)
        for detalle in data["detalles"]
    ]

    return PedidoType(
        id=data["id"],
        cliente_id=data["cliente_id"],
        estado=data["estado"],
        total=data["total"],
        metodo_pago=data["metodo_pago"],
        estado_pago=data["estado_pago"],
        codigo_transaccion=data["codigo_transaccion"],
        detalles=detalles
    )


# Consultas GraphQL
@strawberry.type
class Query:

    @strawberry.field
    async def pedido(
        self,
        info: Info,
        order_id: int
    ) -> Optional[PedidoType]:

        return await obtener_pedido_autorizado(
            info,
            order_id
        )

    @strawberry.field
    async def producto(self, product_id: int) -> Optional[ProductoType]:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{INVENTORY_URL}/products/{product_id}"
                )
        except httpx.RequestError:
            raise ValueError(
                "Inventory Service no está disponible"
            )

        if response.status_code == 404:
            return None

        if response.status_code != 200:
            raise ValueError(
                "Error al consultar Inventory Service"
            )

        data = response.json()

        return ProductoType(**data)

    @strawberry.field
    async def resumen_pedido(
        self,
        info: Info,
        order_id: int
    ) -> Optional[ResumenPedidoType]:

        # Reutilizar la autenticación y autorización existentes
        pedido = await obtener_pedido_autorizado(info, order_id)
        if pedido is None:
            return None

        productos = []
        cache_productos = {}

        async with httpx.AsyncClient(timeout=5.0) as client:
            for detalle in pedido.detalles:

                if detalle.producto_id not in cache_productos:
                    try:
                        respuesta = await client.get(
                            f"{INVENTORY_URL}/products/{detalle.producto_id}"
                        )
                    except httpx.RequestError:
                        raise ValueError(
                            "Inventory Service no está disponible"
                        )

                    if respuesta.status_code != 200:
                        raise ValueError(
                            "No se pudo consultar un producto del pedido"
                        )

                    cache_productos[detalle.producto_id] = respuesta.json()

                producto = cache_productos[detalle.producto_id]

                productos.append(
                    ProductoResumenType(
                        producto_id=detalle.producto_id,
                        nombre=producto["nombre"],
                        cantidad=detalle.cantidad,
                        precio_unitario=detalle.precio_unitario,
                        subtotal=detalle.subtotal
                    )
                )

        return ResumenPedidoType(
            id=pedido.id,
            cliente_id=pedido.cliente_id,
            estado=pedido.estado,
            total=pedido.total,
            metodo_pago=pedido.metodo_pago,
            estado_pago=pedido.estado_pago,
            codigo_transaccion=pedido.codigo_transaccion,
            productos=productos
        )
        
# Aplicación GraphQL

schema = strawberry.Schema(
    query=Query,
    extensions=[
        lambda: QueryDepthLimiter(max_depth=5),
        lambda: AddValidationRules([MaxFieldsRule])
    ]
)

app = FastAPI(
    title="Dulce Hogar - GraphQL Gateway"
)

graphql_app = GraphQLRouter(schema, context_getter=obtener_contexto)

app.include_router(
    graphql_app,
    prefix="/graphql"
)
