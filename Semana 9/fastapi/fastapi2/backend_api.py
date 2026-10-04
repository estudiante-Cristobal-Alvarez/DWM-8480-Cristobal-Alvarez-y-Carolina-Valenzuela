import os
import secrets

from fastapi import (
    FastAPI,
    Header,
    HTTPException,
    Depends
)

from pydantic import BaseModel


app = FastAPI(
    title="Backend API 2",
    description="Servicio de órdenes protegido de Dulce Hogar"
)


INTERNAL_GATEWAY_SECRET = os.getenv(
    "INTERNAL_GATEWAY_SECRET"
)


if not INTERNAL_GATEWAY_SECRET:
    raise RuntimeError(
        "INTERNAL_GATEWAY_SECRET no está configurado"
    )


ORDENES = [
    {
        "id": 1001,
        "cliente": "ana",
        "producto": "Hamburguesa Brioche",
        "cantidad": 2,
        "total": 7380,
        "estado": "pagada"
    },
    {
        "id": 1002,
        "cliente": "Carolina",
        "producto": "Marraqueta Grande",
        "cantidad": 3,
        "total": 6870,
        "estado": "pendiente"
    }
]


class OrdenRequest(BaseModel):
    producto: str
    cantidad: int
    total: int


class EstadoOrdenRequest(BaseModel):
    estado: str


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


def verify_admin(
    x_authenticated_roles: str = Header(default="")
):
    roles = x_authenticated_roles.split(",")

    if "admin" not in roles:
        raise HTTPException(
            status_code=403,
            detail="Se requiere rol administrador"
        )


@app.get(
    "/health",
    dependencies=[Depends(verify_gateway)]
)
def health():
    return {
        "status": "OK",
        "service": "Backend API 2 - Órdenes"
    }


@app.get(
    "/ordenes",
    dependencies=[
        Depends(verify_gateway),
        Depends(verify_admin)
    ]
)
def obtener_ordenes():
    return {
        "ordenes": ORDENES
    }


@app.get(
    "/ordenes/{orden_id}",
    dependencies=[Depends(verify_gateway)]
)
def obtener_orden(
    orden_id: int,
    x_authenticated_user: str = Header(default="")
):
    for orden in ORDENES:
        if orden["id"] == orden_id:
            return {
                "consultado_por": x_authenticated_user,
                "orden": orden
            }

    raise HTTPException(
        status_code=404,
        detail="Orden no encontrada"
    )


@app.post(
    "/ordenes",
    dependencies=[Depends(verify_gateway)]
)
def crear_orden(
    request: OrdenRequest,
    x_authenticated_user: str = Header(default="")
):
    nuevo_id = max(
        orden["id"] for orden in ORDENES
    ) + 1

    nueva_orden = {
        "id": nuevo_id,
        "cliente": x_authenticated_user,
        "producto": request.producto,
        "cantidad": request.cantidad,
        "total": request.total,
        "estado": "pendiente"
    }

    ORDENES.append(nueva_orden)

    return {
        "message": "Orden creada correctamente",
        "orden": nueva_orden
    }


@app.patch(
    "/ordenes/{orden_id}/estado",
    dependencies=[
        Depends(verify_gateway),
        Depends(verify_admin)
    ]
)
def actualizar_estado(
    orden_id: int,
    request: EstadoOrdenRequest
):
    estados_validos = [
        "pendiente",
        "pagada",
        "preparando",
        "lista",
        "entregada",
        "cancelada"
    ]

    if request.estado not in estados_validos:
        raise HTTPException(
            status_code=400,
            detail="Estado de orden no válido"
        )

    for orden in ORDENES:
        if orden["id"] == orden_id:
            orden["estado"] = request.estado

            return {
                "message":
                "Estado actualizado correctamente",
                "orden": orden
            }

    raise HTTPException(
        status_code=404,
        detail="Orden no encontrada"
    )