import os
import httpx
import secrets

from typing import Literal
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field, ConfigDict

from .database import SessionLocal, engine, Base
from .models import Pago


ORDERS_URL = os.getenv(
    "ORDERS_URL",
    "http://127.0.0.1:9002"
)

ORDERS_INTERNAL_SECRET = os.getenv("ORDERS_INTERNAL_SECRET")

PAYMENTS_INTERNAL_SECRET = os.getenv(
    "PAYMENTS_INTERNAL_SECRET"
)


def sincronizar_pago_con_orders(
    pedido_id: int,
    estado_pago: str,
    codigo_transaccion: str | None = None
):
    if not PAYMENTS_INTERNAL_SECRET:
        raise HTTPException(
            status_code=503,
            detail="Clave interna de Payments no configurada"
        )

    try:
        respuesta = httpx.patch(
            f"{ORDERS_URL}/orders/{pedido_id}/pago",
            headers={
                "X-Payments-Secret": PAYMENTS_INTERNAL_SECRET
            },
            json={
                "estado_pago": estado_pago,
                "codigo_transaccion": codigo_transaccion
            },
            timeout=5.0
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar con Orders Service"
        )

    if respuesta.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=(
                "Orders Service rechazó la actualización "
                f"del pago. Código HTTP: {respuesta.status_code}"
            )
        )

    return respuesta.json()


app = FastAPI(
    title="Dulce Hogar - Payments Service",
    description="Microservicio de gestión de pagos simulados",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


# Conexión con SQLite
def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Datos para registrar un pago
class PagoCrear(BaseModel):
    pedido_id: int = Field(gt=0)
    metodo_pago: Literal["efectivo", "transferencia", "tarjeta"]


# Datos para actualizar el estado de un pago
class PagoEstado(BaseModel):
    estado: Literal["aprobado", "rechazado"]



# Datos que devuelve la API
class PagoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pedido_id: int
    monto: int
    metodo_pago: str
    estado: str


# Verificar el servicio
@app.get("/health")
def health():
    return {
        "status": "OK",
        "service": "payments"
    }

def verificar_payments_interno(
    x_payments_secret: str | None = Header(default=None)
):
    clave_esperada = os.getenv("PAYMENTS_INTERNAL_SECRET")

    if not clave_esperada:
        raise HTTPException(
            status_code=503,
            detail="La seguridad interna de Payments no está configurada"
        )

    if (
        not x_payments_secret
        or not secrets.compare_digest(
            x_payments_secret,
            clave_esperada
        )
    ):
        raise HTTPException(
            status_code=403,
            detail="Servicio no autorizado para modificar pagos"
        )

# Consultar todos los pagos
@app.get("/payments", response_model=list[PagoRespuesta])
def obtener_pagos(
    db: Session = Depends(obtener_db),
    _: None = Depends(verificar_payments_interno)
):
    return db.query(Pago).all()


# Consultar un pago por ID
@app.get("/payments/{payment_id}", response_model=PagoRespuesta)
def obtener_pago(
    payment_id: int,
    db: Session = Depends(obtener_db),
    _: None = Depends(verificar_payments_interno)
):
    pago = db.query(Pago).filter(
        Pago.id == payment_id
    ).first()

    if pago is None:
        raise HTTPException(
            status_code=404,
            detail="Pago no encontrado"
        )

    return pago

# Registrar un pago asociado a un pedido
@app.post(
    "/payments",
    status_code=201,
    response_model=PagoRespuesta
)
def crear_pago(
    datos: PagoCrear,
    db: Session = Depends(obtener_db),
    _: None = Depends(verificar_payments_interno)
):
    # Evitar pagos duplicados
    pago_existente = db.query(Pago).filter(
        Pago.pedido_id == datos.pedido_id
    ).first()

    if pago_existente is not None:
        raise HTTPException(
            status_code=409,
            detail="El pedido ya tiene un pago registrado"
        )

    # Consultar el pedido en Orders Service
    if not ORDERS_INTERNAL_SECRET:
        raise HTTPException(
            status_code=503,
            detail="La clave interna de Orders Service no está configurada"
        )

    # Consultar el pedido en Orders Service
    try:
        respuesta = httpx.get(
            f"{ORDERS_URL}/orders/{datos.pedido_id}",
            headers={
                "X-Orders-Secret": ORDERS_INTERNAL_SECRET
            },
            timeout=5.0
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar con Orders Service"
        )

    if respuesta.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    if respuesta.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Error al consultar Orders Service"
        )

    pedido = respuesta.json()

    # Verificar que el método de pago coincida con el pedido
    if datos.metodo_pago.lower() != pedido["metodo_pago"].lower():
        raise HTTPException(
            status_code=400,
            detail="El método de pago no coincide con el registrado en el pedido"
            )

    # Utilizar el total calculado por Orders
    monto = pedido["total"]

    # Crear un pago simulado
    nuevo_pago = Pago(
        pedido_id=datos.pedido_id,
        monto=monto,
        metodo_pago=datos.metodo_pago,
        estado="pendiente"
    )

    try:
        db.add(nuevo_pago)
        db.commit()
        db.refresh(nuevo_pago)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="El pedido ya tiene un pago registrado"
        )

    return nuevo_pago


# Actualizar el estado de un pago simulado
@app.patch(
    "/payments/{payment_id}/estado",
    response_model=PagoRespuesta
)
def actualizar_estado_pago(
    payment_id: int,
    datos: PagoEstado,
    db: Session = Depends(obtener_db),
    _: None = Depends(verificar_payments_interno)
):
    pago = db.query(Pago).filter(
        Pago.id == payment_id
    ).first()

    if pago is None:
        raise HTTPException(
            status_code=404,
            detail="Pago no encontrado"
        )

    if pago.estado != "pendiente":
        raise HTTPException(
            status_code=409,
            detail="Solo se pueden modificar pagos pendientes"
        )

    
    # Referencia interna del pago simulado
    codigo_transaccion = (
        f"PAGO-{pago.id}"
        if datos.estado == "aprobado"
        else None
    )

    # Actualizar primero Orders Service
    sincronizar_pago_con_orders(
        pedido_id=pago.pedido_id,
        estado_pago=datos.estado,
        codigo_transaccion=codigo_transaccion
    )

    # Guardar el nuevo estado en Payments Service
    pago.estado = datos.estado

    try:
        db.commit()
        db.refresh(pago)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=(
                "Orders fue actualizado, pero no se pudo "
                "guardar el estado en Payments. "
                "Se requiere reconciliación."
            )
        )

    return pago
