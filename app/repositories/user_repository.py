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
    
    async def get_users_by_role(self, role: str) -> list:
        """Retrieve all users with a given role (e.g., 'seller')."""
        sellers = await self.collection.find({"role": role}).to_list(length=None)
        return [{**seller, "_id": str(seller["_id"])} for seller in sellers]