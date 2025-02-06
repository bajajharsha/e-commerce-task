from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from app.config.database import database
from app.models.schemas.cart_schema import Order

class CartRepository:
    def __init__(self, cart_collection: AsyncIOMotorCollection = Depends(database.get_db)):
        self.collection: AsyncIOMotorCollection = database.get_cart_collection()

    async def add_cart(self, cart_data: dict):
        result = await self.collection.insert_one(cart_data)
        return result
    
    async def get_cart_by_user_id(self, user_id: str):
        cart_items = await self.collection.find({"user_id": user_id}).to_list(length=100) 
        # make _id a string
        for cart_item in cart_items:
            cart_item["_id"] = str(cart_item["_id"])
        return cart_items
    
    async def clear_cart(self, user_id: str):
        await self.collection.delete_many({"user_id": user_id})