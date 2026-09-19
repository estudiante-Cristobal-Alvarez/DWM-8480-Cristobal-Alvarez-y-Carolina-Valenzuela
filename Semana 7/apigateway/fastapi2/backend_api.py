from fastapi import FastAPI


app = FastAPI(
    title="Backend API en",
    description="API ubicada y enrutada por API gateway"
)


@app.get("/health")
def health():
    return {
        "status": "OK",
        "service": "Backend API 2"
    }


@app.get("/productos")
def productos():
    return {
        "products": [
            {
                "id": 1,
                "name": "Marraqueta",
                "price": 1000
            },
            {
                "id": 2,
                "name": "Hallulla",
                "price": 850
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