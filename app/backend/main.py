from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI()

MONGO_USERNAME = os.getenv("MONGO_USERNAME", "admin")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "password123")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "itemsdb")

MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"

client = AsyncIOMotorClient(MONGO_URI)

db = client[MONGO_DB]


class Item(BaseModel):
    name: str


class ItemResponse(BaseModel):
    id: str
    name: str
    created_at: datetime


@app.on_event("startup")
async def startup():
    try:
        await client.admin.command("ping")
        print("Connected to MongoDB")
    except Exception as e:
        print(f"MongoDB connection error: {e}")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/items")
async def get_items():
    items = []
    async for item in db.items.find():
        items.append({
            "id": str(item["_id"]),
            "name": item["name"],
            "created_at": item["created_at"]
        })
    return items


@app.post("/items", status_code=201)
async def create_item(item: Item):
    new_item = {
        "name": item.name,
        "created_at": datetime.now()
    }
    result = await db.items.insert_one(new_item)
    return {
        "id": str(result.inserted_id),
        "name": new_item["name"],
        "created_at": new_item["created_at"]
    }# trigger
