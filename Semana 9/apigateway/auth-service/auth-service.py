from datetime import datetime, timedelta, timezone
import os
import secrets

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

app = FastAPI(
    tittle="Authentication Service",
    details="Servicio simple de autenticación"
)

USERS = {
    "ana": {
        "password": "1234",
        "user_id": "USR-001",
        "roles": ["user"]
    },
    "Carolina": {
        "password": "5678",
        "user_id": "USR-002",
        "roles": ["user"]
    },
    "Cristóbal": {
        "password": "admin123",
        "user_id": "USR-003",
        "roles": ["user", "admin"]
    },
}

SESSIONS = {}

TOKEN_LIFETIME_TIME = 15

AUTH_INTROSPECTION_SECRET = os.getenv(
    "AUTH_INTROSPECTION_SECRET",
    "demo-introspection-secret"
)

class LoginRequest(BaseModel):
    username: str
    password: str

class IntrospectionRequest(BaseModel):
    token: str

@app.post("/login")
def login(request: LoginRequest):
    user = USERS.get(request.username)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Usuario Incorrecto"
        )
    if user["password"] != request.password:
        raise HTTPException(
            status_code=401,
            detail="Credenciales Incorrectas"
        )
    access_token = secrets.token_urlsafe(32)
    expiration = (datetime.now(timezone.utc) + timedelta(minutes=TOKEN_LIFETIME_TIME))
    #Asociar el token a una identidad
    SESSIONS[access_token] = {
        "user_id": user["user_id"],
        "username": request.username,
        "roles": user["roles"],
        "expires_at": expiration
    }
    return{
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": TOKEN_LIFETIME_TIME * 60
    }

@app.post("/introspect")
def introspect(
    request: IntrospectionRequest,
    x_gateway_auth_secret: str = Header(default="")
):
    if not secrets.compare_digest(
        x_gateway_auth_secret,
        AUTH_INTROSPECTION_SECRET
    ):
        raise HTTPException(
            status_code=403,
            detail="Gateway no autorizado"
        )
    session = SESSIONS.get(request.token)
    if session is None:
        return{
            "active": False
        }
    if (datetime.now(timezone.utc) > session["expires_at"]):
        SESSIONS.pop(request.token, None)
        return{
            "active": False
        }
    return{
        "active": True,
        "user_id": session["user_id"],
        "username": session["username"],
        "roles": session["roles"],
        "expires_at": session["expires_at"].isoformat()
    }

@app.post("/logout")
def loguout(
    request: IntrospectionRequest,
    x_gateway_auth_secret: str = Header(default="")
):
    if not secrets.compare_digest(
        x_gateway_auth_secret,
        AUTH_INTROSPECTION_SECRET
    ):
        raise HTTPException(
            status_code=403,
            detail="Gateway no autorizado"
        )
    SESSIONS.pop(request.token, None)
    return{
        "message": "Sesión finalizada"
    } 

@app.get("/health")
def health(x_gateway_auth_secret: str = Header(default="")):
    if not secrets.compare_digest(
        x_gateway_auth_secret,
        AUTH_INTROSPECTION_SECRET
    ):
        raise HTTPException(
            status_code=403,
            detail="Gateway no autorizado"
        )
    return{
        "status": "OK",
        "service": "Authentication Service"
    } 
