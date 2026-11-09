import os
import secrets

from fastapi import (
    FastAPI,
    Header,
    HTTPException,
    Depends
)


app = FastAPI(
    title="Backend API 2",
    description="Segundo servicio protegido de Dulce Hogar"
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
        "service": "Backend API 2"
    }


@app.get(
    "/ordenes",
    dependencies=[Depends(verify_gateway)]
)
def ordenes():
    return {
        "ordenes": [
            {
                "id": 1001,
                "estado": "pagada"
            },
            {
                "id": 1002,
                "estado": "pendiente"
            }
        ]
    }