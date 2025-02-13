from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from app.config.database import database


class UserRepository:
    def __init__(
        self, user_collection: AsyncIOMotorCollection = Depends(database.get_db)
    ):
        self.collection: AsyncIOMotorCollection = database.get_user_collection()
        self.product_collection: AsyncIOMotorCollection = (
            database.get_products_collection()
        )

    async def get_user_by_email(self, email: str):
        return await self.collection.find_one({"email": email})

    async def create_user(self, user_data: dict):
        result = await self.collection.insert_one(user_data)
        return result.inserted_id

    async def get_admin_emails(self) -> list[str]:
        """Fetch emails of all admins."""
        admins = await self.collection.find(
            {"role": "admin"},  # Filter: Only users with role 'admin'
            {"email": 1, "_id": 0},  # Projection: Include only 'email', exclude '_id'
        ).to_list(None)

        return [admin["email"] for admin in admins]  # Return only email list

    async def get_admin_email(self) -> list[str]:
        """Fetch emails of all admins."""
        admins = await self.collection.find(
            {"role": "admin"}, {"email": 1, "_id": 0}
        ).to_list(None)
        return [admin["email"] for admin in admins]

    async def find_seller(self, product_id: str):
        # Step 1: Find the seller ID associated with the product
        product = await self.product_collection.find_one(
            {"_id": str(product_id)}, {"seller_id": 1}
        )

        if not product or "seller_id" not in product:
            return None  # Return None if product or seller_id is not found

        seller_id = product["seller_id"]

        # Step 2: Fetch the seller's email using the seller ID
        seller = await self.collection.find_one({"_id": seller_id}, {"email": 1})

        if not seller or "email" not in seller:
            return None  # Return None if seller or email is not found

        return seller["email"]  # Return the seller's email
