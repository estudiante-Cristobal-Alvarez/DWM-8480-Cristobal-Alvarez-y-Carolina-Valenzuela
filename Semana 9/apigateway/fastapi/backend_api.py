import os 
import secrets
from fastapi import (
    FastAPI,
    Header,
    HTTPException,
    Depends
)

app = FastAPI(
    title="Backend API",
    description="API ubicada en servidor enrutada por el API Gateway"
)

INTERNAL_GATEWAY_SECRET = os.getenv(
    "INTERNAL_GATEWAY_SECRET"
)


if not INTERNAL_GATEWAY_SECRET:
    raise RuntimeError(
        "INTERNAL_GATEWAY_SECRET no esta configurado"
    )

def verify_gateway(
        x_gateway_secret: str = Header(default="")
):
    valid = secrets.compare_digest(
        x_gateway_secret,
        INTERNAL_GATEWAY_SECRET # type: ignore
    ) # type: ignore
    if not valid:
        raise HTTPException(
            status_code=403, 
            detail="Solicitud no autorizada desde Gateway"
        )

@app.get(
    "/health",
    dependencies=[Depends(verify_gateway)]
)
def health():
    return{
        "status": "OK",
        "services": "Backend API"
    }

@app.get(
    "/products",
    dependencies=[Depends(verify_gateway)]
)

def productos(
    x_authenticaded_client: str | None = Header(default=None),
    x_authenticaded_user: str | None = Header(default=None),
    x_authenticaded_roles: str | None = Header(default=None),

):
    return {
        "identify":{
            "client_id": x_authenticaded_client,
            "username": x_authenticaded_user,
            "roles": x_authenticaded_roles
        },
        "productos": [
            {
                "id": 1,
                "nombre": "Hamburguesa Brioche",
                "categoria": "panaderia",
                "precio": 3690
            },
            {
                "id": 2,
                "nombre": "Marraqueta Grande",
                "categoria": "panaderia",
                "precio": 2290
            }
        ]
    }


    