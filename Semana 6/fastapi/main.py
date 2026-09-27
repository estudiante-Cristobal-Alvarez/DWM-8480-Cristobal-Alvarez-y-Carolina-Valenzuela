from typing import List, Optional, Dict
from itertools import count

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from contextlib import asynccontextmanager

#Configuracion BD mongodb
MONGODB_URI = "mongodb://localhost:27017"
DB_NAME = "bdunab2"
COLL_NAME = "items"

client: AsyncIOMotorClient | None = None
db = None
coll= None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db, coll
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    coll = db[COLL_NAME]
    yield
    client.close()

app = FastAPI(title="FastAPI con MongoDB", version="1.0.0", lifespan=lifespan)

class Item(BaseModel):
    nombre: str = Field(min_length=1, description="Nombre del producto")
    precio: float = Field(gt=0, description="Precio del producto mayor que 0")
    tags: List[str] = Field(default_factory=list)
    activo: bool = True

class ItemIn(BaseModel):
    nombre: str = Field(min_length=1, description="Nombre del producto")
    precio: float = Field(gt=0, description="Precio del producto mayor que 0")
    tags: List[str] = Field(default_factory=list)
    activo: bool = True

class ItemOut(Item):
    id: str

def doc_to_itemout(doc) -> ItemOut:
    return ItemOut(
        id=str(doc["_id"]),
        nombre=doc["nombre"],
        precio=doc["precio"],
        tags=doc.get("tags", []),
        activo=doc.get("activo", True)
    )

#Endpoints
@app.post("/health", tags=["Sistema"])
def health():
    return{"status":"ok"}

@app.get("/items", response_model=List[ItemOut])
async def listar_items(
    q: Optional[str] = Query(None, description="Filtro por nombre que contenga q"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=200),
):

    query = {}
    if q:
        query["nombre"] = {"$regex": q, "$options": "i"}

    cursor = coll.find(query).skip(skip).limit(limit)
    items: List[ItemOut]= []
    async for doc in cursor:
        items.append(doc_to_itemout(doc))
    return items

@app.post("/items", response_model=ItemOut, status_code=201, tags=["items"])
async def crear_item(item: ItemIn):
    res = await coll.insert_one(item.model_dump())
    doc = await coll.find_one({"_id": res.inserted_id})
    return doc_to_itemout(doc)


#Endpoint para contar items activos
@app.get("/items/activos", response_model=int, status_code=200, tags=["items"])
async def contar_items_activos():
    cursor = coll.find({"activo": True})

    items: List[ItemOut] = []

    async for doc in cursor:
        items.append(doc_to_itemout(doc))
    return len(items)

# Buscar items por tag
@app.get("/items/tag/{tag}", response_model=List[ItemOut], status_code=200, tags=["items"])
async def buscar_productos_por_tag(tag: str):
    query ={
        "tags": tag
    }
    cursor = coll.find(query)
    items: List[ItemOut] = []
    async for doc in cursor:
        items.append(doc_to_itemout(doc))
    return items

#localhost:8098/items/2(parámetro de ruta)
@app.get("/items/{item_id}", response_model=ItemOut, status_code=200)
async def obtener_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="id inválido")
    doc = await coll.find_one({"_id": ObjectId(item_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return doc_to_itemout(doc)

@app.put("/items/{item_id}", response_model=ItemOut, status_code=200)
async def actualizar_item(item_id: str, item: ItemIn):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="id inválido")
    res = await coll.update_one(
        {"_id": ObjectId(item_id)}, 
        {"$set": item.model_dump()}
    )
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    doc = await coll.find_one({"_id": ObjectId(item_id)})
    return doc_to_itemout(doc)

@app.delete("/items/{item_id}", status_code=204, tags=["items"])
async def eliminar_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="id inválido")
    res = await coll.delete_one({"_id": ObjectId(item_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return None
