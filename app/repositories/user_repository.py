from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from app.config.database import database

class UserRepository:
    def __init__(self, user_collection: AsyncIOMotorCollection = Depends(database.get_db)):
        self.collection: AsyncIOMotorCollection = database.get_user_collection()

    async def get_user_by_email(self, email: str):
        return await self.collection.find_one({"email": email})

    async def create_user(self, user_data: dict):
        result = await self.collection.insert_one(user_data)
        return result.inserted_id