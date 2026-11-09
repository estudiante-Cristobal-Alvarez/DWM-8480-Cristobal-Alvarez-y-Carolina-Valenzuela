import os
import secrets

from fastapi import Header
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from .database import SessionLocal, engine, Base
from .models import Cliente


app = FastAPI(
    title="Dulce Hogar - Clients Service",
    description="Microservicio de gestión de clientes",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


def verificar_credencial_interna(
    x_clients_secret: str | None = Header(default=None)
):
    clave_configurada = os.getenv("CLIENTS_INTERNAL_SECRET")

    if not clave_configurada:
        raise HTTPException(
            status_code=503,
            detail="La seguridad interna de Clients no está configurada"
        )

    if (
        x_clients_secret is None
        or not secrets.compare_digest(
            x_clients_secret,
            clave_configurada
        )
    ):
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado: credencial interna inválida"
        )

    return True


# Conexión con la base de datos
def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Datos para registrar un cliente
class ClienteCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    correo: EmailStr
    telefono: str | None = Field(default=None, max_length=20)
    direccion: str | None = Field(default=None, max_length=250)


# Datos para actualizar un cliente
class ClienteActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=150)
    correo: EmailStr | None = None
    telefono: str | None = Field(default=None, max_length=20)
    direccion: str | None = Field(default=None, max_length=250)


# Datos que devuelve la API
class ClienteRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    correo: EmailStr
    telefono: str | None
    direccion: str | None


# Verificar el servicio
@app.get("/health")
def health():
    return {
        "status": "OK",
        "service": "clients"
    }


# Consultar todos los clientes
@app.get("/clients", response_model=list[ClienteRespuesta])
def obtener_clientes(
    db: Session = Depends(obtener_db),
    autorizado: bool = Depends(verificar_credencial_interna)
):
    return db.query(Cliente).all()



# Consultar un cliente por ID
@app.get("/clients/{client_id}", response_model=ClienteRespuesta)
def obtener_cliente(
    client_id: int,
    db: Session = Depends(obtener_db),
    autorizado: bool = Depends(verificar_credencial_interna)
):
    cliente = db.query(Cliente).filter(
        Cliente.id == client_id
    ).first()

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    return cliente


# Registrar un cliente
@app.post("/clients", status_code=201, response_model=ClienteRespuesta)
def crear_cliente(
    datos: ClienteCrear,
    db: Session = Depends(obtener_db),
    autorizado: bool = Depends(verificar_credencial_interna)
):

    nuevo_cliente = Cliente(**datos.model_dump())

    try:
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="El correo electrónico ya está registrado"
        )

    return nuevo_cliente


# Actualizar un cliente
@app.put("/clients/{client_id}", response_model=ClienteRespuesta)
def actualizar_cliente(
    client_id: int,
    datos: ClienteActualizar,
    db: Session = Depends(obtener_db),
    autorizado: bool = Depends(verificar_credencial_interna)
):
    cliente = db.query(Cliente).filter(
        Cliente.id == client_id
    ).first()

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    cambios = datos.model_dump(exclude_unset=True)

    for campo, valor in cambios.items():
        setattr(cliente, campo, valor)

    try:
        db.commit()
        db.refresh(cliente)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="El correo electrónico ya está registrado"
        )

    return cliente