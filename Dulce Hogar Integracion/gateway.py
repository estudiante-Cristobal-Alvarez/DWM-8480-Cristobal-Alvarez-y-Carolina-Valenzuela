import os
import secrets
import httpx

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Request,
    Response
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

app = FastAPI(title="API Gateway - Dulce Hogar")

security = HTTPBearer(
    auto_error=False
)

VAULT_ADDR = os.getenv(
    "VAULT_ADDR", "http://localhost:8200"
)

VAULT_TOKEN = os.getenv(
    "VAULT_TOKEN", "dev-only-token"
)

async def get_gateway_secrets():
    url = f"{VAULT_ADDR}/v1/secret/data/gateway"
    headers = {
        "X-Vault-Token": VAULT_TOKEN
    }

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                # Respaldo temporal si Vault no está disponible
                return {
                    "client_token": "dev-token-123",
                    "backend_shared_secret": "gateway-api-secret-456"
                }
            vault_response = response.json()
            return vault_response["data"]["data"]
        except httpx.RequestError:
            # Respaldo por si hay error de conexión con Vault
            return {
                "client_token": "dev-token-123",
                "backend_shared_secret": "gateway-api-secret-456"
            }

async def authenticate_client(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Bearer token requerido"
        )
    vault_secrets = await get_gateway_secrets()
    expected_token = vault_secrets["client_token"]
    received_token = credentials.credentials
    valid = secrets.compare_digest(received_token, expected_token)
    if not valid:
        raise HTTPException(status_code=401, detail="Token inválido")
    return {
        "client_id": "student-client",
        "backend_secret": vault_secrets["backend_shared_secret"]
    }

# Direcciones de los microservicios
BACKEND_URL = "http://localhost:8000"  # Microservicio de productos (main.py)
BACKEND_URL2 = "http://localhost:9100" # Otro microservicio 

@app.api_route(
    "/api/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)
async def proxy(
    path: str,
    request: Request,
    auth=Depends(authenticate_client)
):
    if path.startswith("ordenes"):
        target_url = f"{BACKEND_URL2}/{path}"
    else:
        target_url = f"{BACKEND_URL}/{path}"
        
    body = await request.body()
    
    # Preparamos las cabeceras que se enviarán al microservicio backend
    gateway_headers = {
        "X-Gateway-Secret": auth["backend_secret"],  # Sello secreto automático para pasar el Depends del backend
        "X-Authenticated-Client": auth["client_id"]
    }
    
    # Opcional pero recomendado: si el cliente mandó un token de usuario y quieres reenviarlo
    auth_header = request.headers.get("Authorization")
    if auth_header:
        gateway_headers["Authorization"] = auth_header

    content_type = request.headers.get("content-type")
    if content_type:
        gateway_headers["content-type"] = content_type

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            upstream = await client.request(
                method=request.method,
                url=target_url,
                params=request.query_params,
                content=body,
                headers=gateway_headers
            )
    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Backend no disponible"
        )
        
    response_headers = {}
    if "content-type" in upstream.headers:
        response_headers["content-type"] = upstream.headers["content-type"]
        
    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers=response_headers
    )