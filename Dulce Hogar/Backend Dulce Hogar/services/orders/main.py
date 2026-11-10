import uuid
import os
import httpx
import secrets

from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Literal

from .database import SessionLocal, engine, Base
from .models import Pedido, DetallePedido
from services.orders.grpc_client import consultar_stock_con_grpc


app = FastAPI(
    title="Dulce Hogar - Orders Service",
    description="Microservicio de gestión de pedidos y pagos mediante gRPC y FastAPI",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


# Obtener una sesión de base de datos
def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


CLIENTS_URL = os.getenv("CLIENTS_URL", "http://127.0.0.1:9003")

CLIENTS_INTERNAL_SECRET = os.getenv("CLIENTS_INTERNAL_SECRET")

def validar_cliente(cliente_id: int):
    """Verifica que el cliente exista en Clients Service."""

    try:
        respuesta = httpx.get(
            f"{CLIENTS_URL}/clients/{cliente_id}",
            timeout=5.0
        )
        if not CLIENTS_INTERNAL_SECRET:
            raise HTTPException(
                status_code=503,
                detail="La credencial interna de Clients no está configurada"
            )

        respuesta = httpx.get(
            f"{CLIENTS_URL}/clients/{cliente_id}",
            headers={
                "X-Clients-Secret": CLIENTS_INTERNAL_SECRET
            },
            timeout=5.0
        )


    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Clients Service no está disponible temporalmente"
        )

    if respuesta.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente con ID {cliente_id} no encontrado"
        )

    if respuesta.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Error al consultar Clients Service"
        )

    return respuesta.json()


# Datos necesarios para registrar un pedido y su pago 
class ProductoPedido(BaseModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(gt=0)


class PedidoCrear(BaseModel):
    cliente_id: int = Field(gt=0)
    productos: list[ProductoPedido] = Field(min_length=1)
    metodo_pago: str = Field(..., description="Método de pago del pedido: tarjeta o transferencia")


class PedidoEstado(BaseModel):
    estado: Literal["confirmado", "cancelado"]


class PedidoPagoEstado(BaseModel):
    estado_pago: Literal["aprobado", "rechazado"]
    codigo_transaccion: str | None = None


def verificar_payments(
    x_payments_secret: str | None = Header(default=None)
):
    clave_esperada = os.getenv("PAYMENTS_INTERNAL_SECRET")

    if not clave_esperada:
        raise HTTPException(
            status_code=503,
            detail="Seguridad interna de Payments no configurada"
        )

    if not x_payments_secret or not secrets.compare_digest(
        x_payments_secret, clave_esperada
    ):
        raise HTTPException(
            status_code=403,
            detail="Payments Service no autorizado"
        )

def verificar_orders_interno(
    x_orders_secret: str | None = Header(default=None)
):
    clave_esperada = os.getenv("ORDERS_INTERNAL_SECRET")

    if not clave_esperada:
        raise HTTPException(
            status_code=503,
            detail="Seguridad interna de Orders no configurada"
        )

    if not x_orders_secret or not secrets.compare_digest(
        x_orders_secret,
        clave_esperada
    ):
        raise HTTPException(
            status_code=403,
            detail="Servicio no autorizado para consultar pedidos"
        )

@app.get("/health")
def health():
    return {
        "status": "OK",
        "service": "orders"
    }


@app.get("/orders")
def obtener_pedidos(
    db: Session = Depends(obtener_db),
    _: None = Depends(verificar_orders_interno)
):
    pedidos = db.query(Pedido).all()

    return {
        "total": len(pedidos),
        "pedidos": pedidos
    }


@app.get("/orders/{order_id}")
def obtener_pedido(
    order_id: int,
    db: Session = Depends(obtener_db),
    _: None = Depends(verificar_orders_interno)
):
    pedido = db.query(Pedido).filter(
        Pedido.id == order_id
    ).first()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    detalles = db.query(DetallePedido).filter(
        DetallePedido.pedido_id == order_id
    ).all()

    return {
        "id": pedido.id,
        "cliente_id": pedido.cliente_id,
        "estado": pedido.estado,
        "total": pedido.total,
        "metodo_pago": pedido.metodo_pago,
        "estado_pago": pedido.estado_pago,
        "codigo_transaccion": pedido.codigo_transaccion,

        "detalles": [
            {
                "producto_id": detalle.producto_id,
                "cantidad": detalle.cantidad,
                "precio_unitario": detalle.precio_unitario,
                "subtotal": detalle.subtotal
            }
            for detalle in detalles
        ]
    }


@app.post("/orders", status_code=201)
def crear_pedido(
    pedido: PedidoCrear,
    db: Session = Depends(obtener_db),
    _: None = Depends(verificar_orders_interno)
):
    # Validar tarjeta o transferencia
    metodos_validos = ["tarjeta", "transferencia"]
    if pedido.metodo_pago.lower() not in metodos_validos:
        raise HTTPException(
            status_code=400,
            detail=f"Método de pago inválido. Solo se aceptan pagos online: {metodos_validos}"
        )

    # Limitar la cantidad de productos por pedido
    MAX_PRODUCTOS_POR_PEDIDO = 20

    if not 1 <= len(pedido.productos) <= MAX_PRODUCTOS_POR_PEDIDO:
        raise HTTPException(
            status_code=400,
            detail=(
            f"El pedido debe contener entre 1 y "
            f"{MAX_PRODUCTOS_POR_PEDIDO} productos"
            )
        )
    
    # Verificar que el cliente exista antes de consultar Inventory
    validar_cliente(pedido.cliente_id)
    detalles_calculados = []
    total_pedido = 0

    # Consultar los productos y validar stock en Inventory utilizando gRPC (Se reemplaza HTTP por gRPC)
    for item in pedido.productos:
        resultado_stock = consultar_stock_con_grpc(
            product_id=item.producto_id,
            cantidad=item.cantidad
        )

        if not resultado_stock["disponible"]:
            raise HTTPException(
                status_code=400,
                detail=f"Producto {item.producto_id} no disponible: {resultado_stock['mensaje']}"
            )

        precio = resultado_stock["precio_unitario"]
        subtotal = precio * item.cantidad
        total_pedido += subtotal

        detalles_calculados.append({
            "producto_id": item.producto_id,
            "cantidad": item.cantidad,
            "precio_unitario": precio,
            "subtotal": subtotal
        })

    # Guardar el pedido y sus detalles
    estado_pago_inicial = "pendiente"
    
    # Todavia no existe una transacción de pago que se haya confirmado
    codigo_tx = None

    nuevo_pedido = Pedido(
        cliente_id=pedido.cliente_id,
        estado="pendiente",
        total=total_pedido,
        metodo_pago=pedido.metodo_pago.lower(),
        estado_pago=estado_pago_inicial,
        codigo_transaccion=codigo_tx
    )

    try:
        db.add(nuevo_pedido)
        db.flush()

        for detalle in detalles_calculados:
            nuevo_detalle = DetallePedido(
                pedido_id=nuevo_pedido.id,
                **detalle
            )
            db.add(nuevo_detalle)

        db.commit()
        db.refresh(nuevo_pedido)

    except Exception:
        db.rollback()
        raise

    return {
        "mensaje": "Pedido creado exitosamente utilizando comunicación gRPC con Inventory",
        "pedido": {
            "id": nuevo_pedido.id,
            "cliente_id": nuevo_pedido.cliente_id,
            "estado": nuevo_pedido.estado,
            "total": nuevo_pedido.total,
            "metodo_pago": nuevo_pedido.metodo_pago,
            "estado_pago": nuevo_pedido.estado_pago,
            "codigo_transaccion": nuevo_pedido.codigo_transaccion,
            "detalles": detalles_calculados
        }
    }


@app.patch("/orders/{order_id}/estado")
def actualizar_estado_pedido(
    order_id: int,
    datos: PedidoEstado,
    db: Session = Depends(obtener_db),
    _: None = Depends(verificar_orders_interno)
):
    pedido = db.query(Pedido).filter(
        Pedido.id == order_id
    ).first()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    if pedido.estado != "pendiente":
        raise HTTPException(
            status_code=409,
            detail="Solo se pueden modificar pedidos pendientes"
        )

    pedido.estado = datos.estado

    db.commit()
    db.refresh(pedido)

    return {
        "mensaje": "Estado actualizado correctamente",
        "pedido": {
            "id": pedido.id,
            "cliente_id": pedido.cliente_id,
            "estado": pedido.estado,
            "total": pedido.total,
            "estado_pago": pedido.estado_pago,
        }
    }

@app.patch("/orders/{order_id}/pago")
def actualizar_pago_pedido(
    order_id: int,
    datos: PedidoPagoEstado,
    db: Session = Depends(obtener_db),
    _: None = Depends(verificar_payments)
):
    pedido = db.query(Pedido).filter(
        Pedido.id == order_id
    ).first()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    if pedido.estado_pago != "pendiente":
        raise HTTPException(
            status_code=409,
            detail="El pedido ya tiene un pago procesado"
        )

    if datos.estado_pago == "aprobado" and not datos.codigo_transaccion:
        raise HTTPException(
            status_code=422,
            detail="Se requiere codigo_transaccion para aprobar el pago"
        )

    pedido.estado_pago = datos.estado_pago
    pedido.codigo_transaccion = datos.codigo_transaccion

    db.commit()
    db.refresh(pedido)

    return {
        "mensaje": "Estado de pago actualizado correctamente",
        "pedido": {
            "id": pedido.id,
            "cliente_id": pedido.cliente_id,
            "estado": pedido.estado,
            "total": pedido.total,
            "estado_pago": pedido.estado_pago,
            "codigo_transaccion": pedido.codigo_transaccion
        }
    }