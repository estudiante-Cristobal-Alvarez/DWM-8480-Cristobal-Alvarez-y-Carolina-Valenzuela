from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Auth Service - Dulce Hogar",
    description="Microservicio encargado de la seguridad y entrega de tokens"
)

# Estructura de los datos que necesitamos para iniciar sesión
class LoginRequest(BaseModel):
    usuario: str
    password: str

@app.post("/login")
def iniciar_sesion(datos: LoginRequest):
    # Verificamos si el usuario y la contraseña son correctos
    if datos.usuario == "caro" and datos.password == "dulce123":
        return {
            "mensaje": "¡Autenticación exitosa!",
            "access_token": "dev-token-123", # Este es el token que va a usar el gateway
            "token_type": "bearer"
        }
    
    # Si fallan, rechazamos la entrada
    raise HTTPException(
        status_code=401,
        detail="Usuario o contraseña incorrectos"
    )