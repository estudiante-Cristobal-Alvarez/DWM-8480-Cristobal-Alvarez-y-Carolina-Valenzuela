import os
from datetime import datetime, timedelta, timezone
import jwt
import httpx


from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from sqlalchemy import select
from pwdlib import PasswordHash

from .database import SessionLocal, engine, Base
from .models import Usuario

# Configuración de HashiCorp Vault
VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")

# Configuración JWT
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30


def obtener_clave_jwt():
    if not VAULT_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="El token de Vault no está configurado"
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
        raise HTTPException(
            status_code=503,
            detail="No se pudo obtener la clave JWT desde Vault"
        ) from error

def crear_token_acceso(usuario: Usuario) -> str:
    ahora = datetime.now(timezone.utc)

    datos_token = {
    "sub": str(usuario.id),
    "correo": usuario.correo,
    "rol": usuario.rol,
    "iat": ahora,
    "exp": ahora + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    }

    token = jwt.encode(
        datos_token,
        obtener_clave_jwt(),
        algorithm=JWT_ALGORITHM
    )

    return token

app = FastAPI(
    title="Dulce Hogar - Auth Service",
    description="Servicio de autenticación de usuarios",
    version="1.0.0"
)

# Crear las tablas si todavía no existen
Base.metadata.create_all(bind=engine)

# Administrador de contraseñas con Argon2
password_hash = PasswordHash.recommended()


# Obtener una sesión de base de datos
def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Datos que recibimos para registrar un usuario
class RegistroUsuario(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    correo: EmailStr
    password: str = Field(min_length=8, max_length=128)


# Datos que devolvemos al registrar un usuario
class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    rol: str
    activo: bool


class LoginUsuario(BaseModel):
    correo: EmailStr
    password: str


@app.get("/health")
def health():
    return {
        "status": "OK",
        "service": "auth-service"
    }


@app.post(
    "/register",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_201_CREATED
)
def registrar_usuario(
    datos: RegistroUsuario,
    db: Session = Depends(obtener_db)
):
    correo = str(datos.correo).lower()

    # Comprobar si el correo ya está registrado
    usuario_existente = db.scalar(
        select(Usuario).where(Usuario.correo == correo)
    )

    if usuario_existente:
        raise HTTPException(
            status_code=409,
            detail="El correo ya está registrado"
        )

    # Proteger la contraseña con Argon2
    hash_seguro = password_hash.hash(datos.password)

    # Crear el usuario con rol cliente
    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        correo=correo,
        password_hash=hash_seguro,
        rol="cliente",
        activo=True
    )

    db.add(nuevo_usuario)

    try:
        db.commit()
        db.refresh(nuevo_usuario)
    except Exception:
        db.rollback()
        raise

    return nuevo_usuario


@app.post("/login")
def iniciar_sesion(
    datos: LoginUsuario,
    db: Session = Depends(obtener_db)
):
    correo = str(datos.correo).lower()

    # Buscar al usuario por correo
    usuario = db.scalar(
        select(Usuario).where(Usuario.correo == correo)
    )

    # Comprobar que el usuario exista y su contraseña sea correcta
    if usuario is None or not password_hash.verify(
        datos.password,
        usuario.password_hash if usuario else password_hash.hash("dummy-password")
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    # Comprobar que la cuenta esté activa
    if not usuario.activo:
        raise HTTPException(
            status_code=403,
            detail="La cuenta está desactivada"
        )

        # Generar token JWT después de validar las credenciales
    token_acceso = crear_token_acceso(usuario)

    return {
        "mensaje": "Inicio de sesión exitoso",
        "access_token": token_acceso,
        "token_type": "bearer",
        "expires_in": JWT_EXPIRATION_MINUTES * 60,
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "rol": usuario.rol
        }
    }
