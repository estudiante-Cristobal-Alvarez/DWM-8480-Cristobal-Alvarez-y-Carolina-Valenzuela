from fastapi import FastAPI


app = FastAPI(
    title="Backend API es",
    description="API ubicada y enrutada por API gateway"
)


@app.get("/health")
def health():
    return {
        "status": "OK",
        "service": "Backend API"
    }


@app.get("/products")
def products():
    return {
        "products": [
            {
                "id": 1,
                "nombre": "Marraqueta",
                "precio": 1000
            },
            {
                "id": 2,
                "nombre": "Hallulla",
                "precio": 850
            }
        ]
    }


@app.get("/orders")
def orders():
    return {
        "ordenes": [
            {
                "id": 1001,
                "status": "paid"
            },
            {
                "id": 1002,
                "status": "pending"
            }
        ]
    }
