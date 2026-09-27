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
    description="API ubicada en servidor enrutada por API Gateway"
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
        INTERNAL_GATEWAY_SECRET
    )

    if not valid:
        raise HTTPException(
            status_code=403,
            detail="Solicitud no autorizada desde gateway"
        )


@app.get(
    "/health",
    dependencies=[Depends(verify_gateway)]
)
def health():
    return {
        "status": "OK",
        "service": "Backend API"
    }

@app.get(
    "/products",
    dependencies=[Depends(verify_gateway)]
)

def productos():
    return {
        "productos": [
            {"id": 1, "nombre": "Notebook", "precio": 900000},
            {"id": 2, "nombre": "Monitor", "precio": 250000}
        ]
    }

@app.get(
    "/products/{product_id}",
    dependencies=[Depends(verify_gateway)]
)
def producto(product_id: int):

    if product_id == 1:
        return {
            "id": 1,
            "nombre": "Notebook",
            "precio": 900000
        }

    if product_id == 2:
        return {
            "id": 2,
            "nombre": "Monitor",
            "precio": 250000
        }

    raise HTTPException(
        status_code=404,
        detail="Producto no encontrado"
    )