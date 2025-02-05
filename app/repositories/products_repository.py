# app/repositories/products_repository.py
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import Depends
from app.config.database import database
from bson import ObjectId

class ProductsRepository:
    def __init__(self, db: AsyncIOMotorCollection = Depends(database.get_db)):
        self.collection: AsyncIOMotorCollection = database.get_products_collection()

    async def get_all_products(self):
        """Retrieve all products from the database."""
        products = await self.collection.find().to_list(length=None)
        
        # Convert ObjectId to string for serialization
        for product in products:
            product["_id"] = str(product["_id"])
            product["seller_id"] = str(product["seller_id"])

        return products

    async def save_products(self, products: list) -> None:
        """Insert multiple products into the database."""
        if products:
            await self.collection.insert_many(products)

    async def get_product_by_id(self, product_id: str):
        """Retrieve a single product by its ObjectId."""
        if not ObjectId.is_valid(product_id):
            return None

        product = await self.collection.find_one({"_id": product_id})

        if product:
            product["_id"] = str(product["_id"])  # Convert ObjectId to string
            return {k: v for k, v in product.items() if v is not None}  # Exclude None values

        return None
