# app/repositories/products_repository.py
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import Depends
from app.config.database import database
from bson import ObjectId
from app.models.schemas.products_schema import ProductUpdateSchema

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
        # print(products)

        """Insert multiple products into the database."""
        if products:
            await self.collection.insert_many(products)
            
    async def create_product(self, product: dict) -> str:
        product["_id"] = str(ObjectId())  
        result = await self.collection.insert_one(product)
        product["_id"] = str(result.inserted_id)
        return product

    async def get_product_by_id(self, product_id: str):
        """Retrieve a single product by its ObjectId."""
        if not ObjectId.is_valid(product_id):
            return None

        product = await self.collection.find_one({"_id": product_id})

        if product:
            product["_id"] = str(product["_id"])  # Convert ObjectId to string
            return {k: v for k, v in product.items() if v is not None}  # Exclude None values

        return None
    
    async def update_product(self, product_id: str, product_data: ProductUpdateSchema):
        product_object_id = product_id
        update_data = product_data.dict(exclude_unset=True)  # Only update the fields that are provided
        
        # Find and update the product in the database
        updated_product = await self.collection.find_one_and_update(
            {"_id": product_object_id},
            {"$set": update_data},
            return_document=True  # Return the updated document
        )
        
        return updated_product
