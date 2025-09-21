from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from bson import ObjectId
import os

# ---------------------
# Pydantic モデル
# ---------------------


class ItemBase(BaseModel):
    name: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True


# ---------------------
# FastAPI アプリ & DB接続
# ---------------------

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    mongo_url = os.getenv("MONGO_URL", "mongodb://mongo:27017")
    app.mongodb_client = AsyncIOMotorClient(mongo_url)
    app.mongodb = app.mongodb_client["testdb"]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


# ---------------------
# CRUD エンドポイント
# ---------------------


# Create
@app.post("/items/", response_model=Item)
async def create_item(item: ItemCreate):
    result = await app.mongodb["items"].insert_one(item.dict())
    new_item = await app.mongodb["items"].find_one({"_id": result.inserted_id})
    new_item["_id"] = str(new_item["_id"])  # ← ここで変換
    return Item(**new_item)


# Read all
@app.get("/items/", response_model=list[Item])
async def read_items():
    items = await app.mongodb["items"].find().to_list(100)
    for item in items:
        item["_id"] = str(item["_id"])  # ← ここで変換
    return [Item(**i) for i in items]


# Delete all
@app.delete("/items/")
async def delete_all_items():
    delete_result = await app.mongodb["items"].delete_many({})
    return {"deleted_count": delete_result.deleted_count}
