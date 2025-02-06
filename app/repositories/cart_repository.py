from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from app.config.database import database

class CartRepository:
    def __init__(self, cart_collection: AsyncIOMotorCollection = Depends(database.get_db)):
        self.collection: AsyncIOMotorCollection = database.get_cart_collection()

    async def add_cart(self, cart_data: dict):
        result = await self.collection.insert_one(cart_data)
        return result
    