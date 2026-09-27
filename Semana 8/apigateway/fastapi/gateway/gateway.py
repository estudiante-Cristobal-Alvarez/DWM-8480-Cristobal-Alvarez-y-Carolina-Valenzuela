import os
import secrets
import httpx

# Vault server - Backend   -> Se llaman externamente para request y response


from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Request,
    Response
)

from fastapi.security import(
    HTTPBearer, #Validar la autorización de un token.
    HTTPAuthorizationCredentials
)

app = FastAPI(title="Local API Gateway")

security = HTTPBearer(
    auto_error=False
)

VAULT_ADDR = os.getenv( # SELINUX  -> Capacidad de negarse el acceso a sí mismo
    "VAULT_ADDR", "http://localhost:8200"
)

VAULT_TOKEN = os.getenv(
    "VAULT_TOKEN" #dev-only-token
)

if not VAULT_TOKEN:
    raise RuntimeError(
        "VAULT TOKEN no está configurado"
    )

async def get_gateway_secrets():
    url = (
        f"{VAULT_ADDR}" # http://localhost:8200
        "/v1/secret/data/gateway"
    )
    headers={
        "X-Vault-Token": VAULT_TOKEN # dev-only-token
    }

    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(
            url,   # Como esta en formato json, se puede dejar como url o url=url 
            headers=headers # type: ignore
        ) 
    if response.status_code  != 200:
        raise HTTPException(
            status_code=500,
            detail=f"No fue posible acceder a Vault: {response}"
        )
    vault_response = response.json()
    return vault_response["data"]["data"]

async def authenticate_client(
        credentials: HTTPAuthorizationCredentials = Depends(security)
 ):
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Bearer token requerido"
        )
    vault_secrets =(
        await get_gateway_secrets() #client_token backend_shared_secret
    )
    expected_token = vault_secrets["client_token"]
    received_token = credentials.credentials
    valid = secrets.compare_digest(received_token, expected_token)
    if not valid:
        raise HTTPException(status_code=401, detail="Token inválido")
    return{
        "client_id": "student-client", # Servicios Autenticación e identificación del usuario
        "backend_secret": vault_secrets["backend_shared_secret"]
    }


BACKEND_URL = "http://localhost:9000" #fastapi
BACKEND_URL2 = "http://localhost:9100" #fastapi2

@app.api_route(
    "/api/{path:path}", #product health orders
    methods=["GET","POST","PUT","PATCH","DELETE"]
)
async def proxy(
    path: str,
    request: Request,
    auth=Depends(authenticate_client)
):
    target_url = (
        f"{BACKEND_URL}/{path}" # Call http://localhost_8000/api/products -> http://localhost:9000/products
    )
    body = await request.body()
    gateway_headers ={
        "X-Gateway-Secret":
        auth["backend_secret"], # gateway-api-secret-456
        "X-Authenticated-Client":
        auth["client_id"] # student-client -> Autenticador
    }
    content_type = request.headers.get("content-type")
    if content_type:
        gateway_headers["content_type"] = content_type
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            upstream = await client.request(   # <-- Se hace la llamada al backend
                method=request.method, # GET POST PUT PATCH DELETE
                url = target_url, # "http//localhost:9000/products"
                params=request.query_params, # "http//localhost:9000/products?var1=3&var2=6    A partir del simbolo pregunta es el query_params y se convierten en variables
                content=body,
                headers=gateway_headers
            )
    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Backend no disponible"
        )
    response_headers ={}
    if "content-type" in upstream.headers:
        response_headers["content-type"] = upstream.headers["content-type"]
    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers=response_headers
    )
