from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .database import SessionLocal, engine, Base
from .models import Producto


app = FastAPI(
    title="Dulce Hogar - Inventory Service",
    description="Microservicio de inventario y productos",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


# Obtener sesión de base de datos
def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Datos que recibe la API
class ProductoCrear(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    categoria: str = Field(min_length=1, max_length=50)
    precio: int = Field(gt=0)
    disponible: bool = True


@app.get("/health")
def health():
    return {
        "status": "OK",
        "service": "inventory"
    }


@app.get("/products")
def obtener_productos(db: Session = Depends(obtener_db)):
    productos = db.query(Producto).all()

    return {
        "total": len(productos),
        "productos": productos
    }


@app.get("/products/{product_id}")
def obtener_producto(
    product_id: int,
    db: Session = Depends(obtener_db)
):
    producto = db.query(Producto).filter(
        Producto.id == product_id
    ).first()

    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto


@app.post("/products", status_code=201)
def crear_producto(
    producto: ProductoCrear,
    db: Session = Depends(obtener_db)
):
    nuevo_producto = Producto(
        nombre=producto.nombre,
        categoria=producto.categoria,
        precio=producto.precio,
        disponible=producto.disponible
    )

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return {
        "mensaje": "Producto creado correctamente",
        "producto": nuevo_producto
    }


@app.put("/products/{product_id}")
def actualizar_producto(
    product_id: int,
    producto: ProductoCrear,
    db: Session = Depends(obtener_db)
):
    producto_existente = db.query(Producto).filter(
        Producto.id == product_id
    ).first()

    if producto_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    producto_existente.nombre = producto.nombre
    producto_existente.categoria = producto.categoria
    producto_existente.precio = producto.precio
    producto_existente.disponible = producto.disponible

    db.commit()
    db.refresh(producto_existente)

    return {
        "mensaje": "Producto actualizado correctamente",
        "producto": producto_existente
    }


@app.delete("/products/{product_id}")
def eliminar_producto(
    product_id: int,
    db: Session = Depends(obtener_db)
):
    producto = db.query(Producto).filter(
        Producto.id == product_id
    ).first()

    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    producto_eliminado = {
        "id": producto.id,
        "nombre": producto.nombre,
        "categoria": producto.categoria,
        "precio": producto.precio,
        "disponible": producto.disponible
    }

    db.delete(producto)
    db.commit()

    return {
        "mensaje": "Producto eliminado correctamente",
        "producto": producto_eliminado
    }