from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Producto

# Crear las tablas si todavía no existen
Base.metadata.create_all(bind=engine)

# Código secreto compartido entre el Gateway y este microservicio
SECRET_SHARED = "gateway-api-secret-456"

# Revisa si la petición viene sellada por el gateway
def verificar_origen_gateway(x_gateway_secret: str = Header(None)):
    if x_gateway_secret != SECRET_SHARED:
        raise HTTPException(
            status_code=403, 
            detail="Acceso denegado. Intento de acceso directo sin pasar por el Gateway."
        )
    return x_gateway_secret


# Obtener una sesión de base de datos por solicitud
def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="API Dulce Hogar",
    description="Backend del sistema de ventas online Dulce Hogar",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de Dulce Hogar"
    }


@app.get("/health")
def health():
    return {
        "status": "OK",
        "service": "Backend Dulce Hogar"
    }

@app.get("/products", dependencies=[Depends(verificar_origen_gateway)])
def obtener_productos(db: Session = Depends(obtener_db)):
    productos = db.query(Producto).all()
    return {
        "total": len(productos),
        "productos": productos
    }

class ProductoCrear(BaseModel):
    nombre: str = Field(min_length=2)
    categoria: str = Field(min_length=2)
    precio: int = Field(gt=0)
    disponible: bool = True

@app.get("/products/{product_id}", dependencies=[Depends(verificar_origen_gateway)])
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

@app.post("/products", status_code=201, dependencies=[Depends(verificar_origen_gateway)])
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

@app.put("/products/{product_id}", dependencies=[Depends(verificar_origen_gateway)])
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

@app.delete("/products/{product_id}", dependencies=[Depends(verificar_origen_gateway)])
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