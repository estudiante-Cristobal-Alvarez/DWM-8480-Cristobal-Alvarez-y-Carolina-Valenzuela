from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from .database import SessionLocal, engine, Base
from .models import Pedido


app = FastAPI(
    title="Dulce Hogar - Orders Service",
    description="Microservicio de gestión de pedidos",
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


# Datos necesarios para registrar un pedido
class PedidoCrear(BaseModel):
    cliente_id: int = Field(gt=0)
    total: int = Field(gt=0)


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

    return pedido


@app.post("/orders", status_code=201)
def crear_pedido(
    pedido: PedidoCrear,
    db: Session = Depends(obtener_db)
):
    nuevo_pedido = Pedido(
        cliente_id=pedido.cliente_id,
        estado="pendiente",
        total=pedido.total
    )

    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)

    return {
        "mensaje": "Pedido creado correctamente",
        "pedido": nuevo_pedido
    }