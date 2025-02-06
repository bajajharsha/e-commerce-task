# from fastapi import Depends
# from motor.motor_asyncio import AsyncIOMotorCollection
# from app.config.database import database
# # from models.domain.complaint import Complaint
# from typing import List

# class ComplaintRepository:
#     def __init__(self, complaint_collection: AsyncIOMotorCollection = Depends(database.get_complaint_collection)):
#         self.collection: AsyncIOMotorCollection = complaint_collection

#     async def create_complaint(self, complaint_data: dict):
#         """Create a new complaint record in the database"""
#         result = await self.collection.insert_one(complaint_data)
#         return str(result.inserted_id)
