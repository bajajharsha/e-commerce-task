# from models.domain.complaint import Complaint
from bson import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from app.config.database import database


class ComplaintRepository:
    def __init__(
        self,
        complaint_collection: AsyncIOMotorCollection = Depends(
            database.get_complaint_collection
        ),
    ):
        self.collection: AsyncIOMotorCollection = complaint_collection

    async def create_complaint(self, complaint_data: dict):
        """Create a new complaint record in the database"""
        complaint_data["product_id"] = ObjectId(complaint_data["product_id"])
        complaint_data["user_id"] = ObjectId(complaint_data["user_id"])
        result = await self.collection.insert_one(complaint_data)
        return str(result.inserted_id)
