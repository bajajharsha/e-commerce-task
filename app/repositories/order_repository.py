from motor.motor_asyncio import AsyncIOMotorCollection
from app.config.database import database
from app.models.schemas.cart_schema import Order
from fastapi import Depends

class OrderRepository:
    def __init__(self, order_collection: AsyncIOMotorCollection = Depends(database.get_db)):
        self.collection: AsyncIOMotorCollection = database.get_order_collection()

    async def create_order(self, order: Order):
        result = await self.collection.insert_one(order.dict())
        # result = str(result.inserted_id)
        # result["_id"] = str(result)
        return result
    