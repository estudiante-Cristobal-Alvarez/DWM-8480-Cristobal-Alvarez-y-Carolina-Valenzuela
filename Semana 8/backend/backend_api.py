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
            },
            {
                "id": 3,
                "nombre": "Pan amasado",
                "categoria": "panaderia",
                "precio": 1500
            },
            {
                "id": 4,
                "nombre": "Empanada de pino",
                "categoria": "empanadas",
                "precio": 2500
            },
            {
                "id": 5,
                "nombre": "Torta de chocolate",
                "categoria": "pasteleria",
                "precio": 18000
            },
            {
                "id": 6,
                "nombre": "Croissant",
                "categoria": "bolleria",
                "precio": 1800
            }
        ]
    }


@app.get(
    "/categories",
    dependencies=[Depends(verify_gateway)]
)
def categorias():
    return {
        "categorias": [
            {"id": 1, "nombre": "panaderia"},
            {"id": 2, "nombre": "pasteleria"},
            {"id": 3, "nombre": "empanadas"},
            {"id": 4, "nombre": "bolleria"},
            {"id": 5, "nombre": "bebidas"}
        ]
    }


@app.get(
    "/products/available",
    dependencies=[Depends(verify_gateway)]
)
def productos_disponibles():
    return {
        "productos": [
            {
                "id": 1,
                "nombre": "Hamburguesa Brioche",
                "precio": 3690,
                "disponible": True
            },
            {
                "id": 2,
                "nombre": "Marraqueta Grande",
                "precio": 2290,
                "disponible": True
            },
            {
                "id": 3,
                "nombre": "Pan amasado",
                "precio": 1500,
                "disponible": True
            },
            {
                "id": 4,
                "nombre": "Empanada de pino",
                "precio": 2500,
                "disponible": False
            },
            {
                "id": 5,
                "nombre": "Torta de chocolate",
                "precio": 18000,
                "disponible": False
            },
            {
                "id": 6,
                "nombre": "Croissant",
                "precio": 1800,
                "disponible": True
            }
        ]
    }


@app.get(
    "/orders",
    dependencies=[Depends(verify_gateway)]
)
def pedidos():
    return {
        "pedidos": [
            {
                "id": 1,
                "cliente": "Carolina",
                "producto": "Pan amasado",
                "cantidad": 2,
                "total": 3000,
                "estado": "Preparando"
            },
            {
                "id": 2,
                "cliente": "Alejandro",
                "producto": "Torta de chocolate",
                "cantidad": 1,
                "total": 18000,
                "estado": "Entregado"
            },
            {
                "id": 3,
                "cliente": "Benjamín",
                "producto": "Empanada de pino",
                "cantidad": 4,
                "total": 10000,
                "estado": "Pendiente"
            },
            {
                "id": 4,
                "cliente": "Isaías",
                "producto": "Croissant",
                "cantidad": 3,
                "total": 5400,
                "estado": "Preparando"
            },
            {
                "id": 5,
                "cliente": "Valentina",
                "producto": "Marraqueta Grande",
                "cantidad": 2,
                "total": 4580,
                "estado": "Entregado"
            },
            {
                "id": 6,
                "cliente": "Camila",
                "producto": "Hamburguesa Brioche",
                "cantidad": 2,
                "total": 7380,
                "estado": "Pendiente"
            }
        ]
    }