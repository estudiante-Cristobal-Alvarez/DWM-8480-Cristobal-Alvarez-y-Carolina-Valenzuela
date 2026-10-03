from fastapi import FastAPI
import httpx


app = FastAPI(title="Local API Gateway")


BACKEND_URL = "http://localhost:9000"
BACKEND_URL2 = "http://localhost:9100"


# Productos del primer backend
@app.get("/api/products")
async def products():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/products"
        )

    return response.json()


# Productos del segundo backend
@app.get("/api/productos")
async def productos():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL2}/productos"
        )

    return response.json()


# Órdenes del primer backend
@app.get("/api/orders")
async def orders():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/orders"
        )

    return response.json()


# Estado del primer backend
@app.get("/api/health")
async def health():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/health"
        )

    return response.json()


# Estado del segundo backend
@app.get("/api/health2")
async def health2():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL2}/health"
        )

    return response.json()