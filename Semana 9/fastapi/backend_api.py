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
    description="Servicio de productos de Dulce Hogar"
)


INTERNAL_GATEWAY_SECRET = os.getenv(
    "INTERNAL_GATEWAY_SECRET"
)


if not INTERNAL_GATEWAY_SECRET:
    raise RuntimeError(
        "INTERNAL_GATEWAY_SECRET no está configurado"
    )


PRODUCTOS = [
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
        "nombre": "Hallulla",
        "categoria": "panaderia",
        "precio": 1990
    },
    {
        "id": 4,
        "nombre": "Torta Chocolate",
        "categoria": "pasteleria",
        "precio": 15990
    },
    {
        "id": 5,
        "nombre": "Pie de Limón",
        "categoria": "pasteleria",
        "precio": 12990
    }
]


def verify_gateway(
    x_gateway_secret: str = Header(default="")
):
    valid = secrets.compare_digest(
        x_gateway_secret,
        INTERNAL_GATEWAY_SECRET  # type: ignore
    )

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
    return {
        "status": "OK",
        "service": "Backend API Productos"
    }


@app.get(
    "/products",
    dependencies=[Depends(verify_gateway)]
)
def productos(
    categoria: str | None = None,
    x_authenticated_client: str | None = Header(default=None),
    x_authenticated_user: str | None = Header(default=None),
    x_authenticated_roles: str | None = Header(default=None)
):
    productos_filtrados = PRODUCTOS

    if categoria:
        productos_filtrados = [
            producto
            for producto in PRODUCTOS
            if producto["categoria"].lower()
            == categoria.lower()
        ]

    return {
        "identity": {
            "client_id": x_authenticated_client,
            "username": x_authenticated_user,
            "roles": x_authenticated_roles
        },
        "productos": productos_filtrados
    }


@app.get(
    "/products/{product_id}",
    dependencies=[Depends(verify_gateway)]
)
def obtener_producto(
    product_id: int
):
    for producto in PRODUCTOS:
        if producto["id"] == product_id:
            return producto

    raise HTTPException(
        status_code=404,
        detail="Producto no encontrado"
    )