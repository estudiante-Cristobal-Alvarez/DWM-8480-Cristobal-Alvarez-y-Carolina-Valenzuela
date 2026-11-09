import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import httpx
from typing import List, Optional

# 1. Definimos los Tipos de Datos (Object Types)
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
    codigo_transaccion: str
    # Agregamos la lista de detalles aquí para que coincida con el JSON de Orders
    detalles: List[DetallePedidoType]

# 2. Definimos las Consultas (Queries)
@strawberry.type
class Query:
    
    @strawberry.field
    async def pedido(self, order_id: int) -> PedidoType:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/orders/{order_id}")
            if response.status_code != 200:
                raise Exception(f"No se pudo encontrar el pedido {order_id} en Orders")
            data = response.json()
            return PedidoType(**data)

    @strawberry.field
    async def producto(self, product_id: int) -> ProductoType:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:9001/products/{product_id}")
            if response.status_code != 200:
                raise Exception(f"No se pudo encontrar el producto {product_id} in Inventory")
            data = response.json()
            return ProductoType(**data)

# 3. Esquema y FastAPI
schema = strawberry.Schema(query=Query)
app = FastAPI(title="Dulce Hogar - GraphQL Gateway")
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")