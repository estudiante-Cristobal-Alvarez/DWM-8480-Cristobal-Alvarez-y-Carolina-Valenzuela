import uuid  # sirve para crear un identificador único para cada pedido

from fastapi import FastAPI, Depends, HTTPException
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


@app.get("/health")
def health():
    return {
        "status": "OK",
        "service": "orders"
    }


@app.get("/orders")
def obtener_pedidos(db: Session = Depends(obtener_db)):
    pedidos = db.query(Pedido).all()

    return {
        "total": len(pedidos),
        "pedidos": pedidos
    }


@app.get("/orders/{order_id}")
def obtener_pedido(
    order_id: int,
    db: Session = Depends(obtener_db)
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
    db: Session = Depends(obtener_db)
):
    # Validar tarjeta o transferencia
    metodos_validos = ["tarjeta", "transferencia"]
    if pedido.metodo_pago.lower() not in metodos_validos:
        raise HTTPException(
            status_code=400,
            detail=f"Método de pago inválido. Solo se aceptan pagos online: {metodos_validos}"
        )
    
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
    estado_pago_inicial = "pagado"
    codigo_tx = f"TXN-{uuid.uuid4().hex[:10].upper()}"  # genera un código de transacción único

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
    db: Session = Depends(obtener_db)
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