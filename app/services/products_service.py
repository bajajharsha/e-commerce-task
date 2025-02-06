# app/services/products_service.py
import httpx
import random
from fastapi import HTTPException, Depends, status, UploadFile
from typing import List
from app.repositories.products_repository import ProductsRepository
from app.repositories.user_repository import UserRepository
from app.models.domain.products import Product
from bson import ObjectId
from app.models.schemas.response_schema import BaseResponse
from app.models.schemas.products_schema import ProductUpdateSchema, ProductCreateSchema
from app.utils.cloud_storage import upload_to_cloud
from app.utils.auth import get_current_user

class ProductsService:
    def __init__(
        self, 
        products_repo: ProductsRepository = Depends(), 
        user_repo: UserRepository = Depends()
    ):
        self.products_repo = products_repo
        self.user_repo = user_repo

    async def get_products(self):
        products = await self.products_repo.get_all_products()
        return BaseResponse(
            data=products,
            message="All products fetched.",
            code=status.HTTP_200_OK,
            error=None
        )

    async def preload_products(self) -> List[dict]:
        try:
            # Fetch products from external API
            products_data = await self.fetch_products_from_external_api()

            # Fetch sellers from DB
            sellers = await self.user_repo.get_users_by_role("seller")
            if not sellers:
                raise HTTPException(status_code=404, detail="No sellers found")

            # Assign products to random sellers
            assigned_products = []
            for product in products_data.get("products", []):
                seller_id = random.choice(sellers)["_id"]

                # Create a Product object
                new_product = Product(
                    title=product.get("title", "Unknown Title"),
                    description=product.get("description", "No description available"),
                    category=product.get("category", "Uncategorized"),
                    price=float(product.get("price", 0.0)),  # Default to 0.0 if missing
                    rating=float(product.get("rating", 0.0)),  # Default to 0.0 if missing
                    brand=product.get("brand", "Unknown Brand"),  # Prevent crash
                    images=product.get("images", []),  # Default to empty list
                    thumbnail=product.get("thumbnail", ""),
                    seller_id=ObjectId(seller_id)  # Ensure it's an ObjectId
                )

                # Convert to dictionary and append
                assigned_products.append(new_product.to_dict())
            # Save to database
            await self.products_repo.save_products(assigned_products)
            
            # return assigned_products
            return BaseResponse(
                data=assigned_products,
                message="Products preloaded successfully",
                code=status.HTTP_200_OK
            )

        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"API Error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    async def fetch_products_from_external_api(self) -> dict:
        """Fetch products from an external API."""
        try:
            external_api_url = "https://dummyjson.com/products"
            async with httpx.AsyncClient() as client:
                response = await client.get(external_api_url)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"API Error: {e}")
        
    async def get_product_by_id(self, product_id):
        result = await self.products_repo.get_product_by_id(product_id)
        if result is None:
            return BaseResponse(
            data=result,
            message="No data Found",
            code=status.HTTP_200_OK,
            error=None
            )
        return BaseResponse(
            data=result,
            message="Fetched product successfully",
            code=status.HTTP_200_OK,
            error=None
        )
        
    async def update_product(self, product_id: str, product_data: ProductUpdateSchema):
        result = await self.products_repo.update_product(product_id, product_data)
        if result is None:
            return BaseResponse(
            data=result,
            message="No data Found",
            code=status.HTTP_200_OK,
            error=None
            )
            
        return BaseResponse(
            data=result,
            message="Data Updated Successfully",
            code=status.HTTP_200_OK,
            error=None
        )

    async def create_product(self, product_data: ProductCreateSchema, image: UploadFile, seller_id):
        # seller_id = get_current_user()
        # Upload image to cloud
        image_url = await upload_to_cloud(image)
        
        # Create product dict with image URL
        product_dict = product_data.dict()
        product_dict["images"] = [image_url]
        product_dict["seller_id"] = str(seller_id)
        
        # # Save to database
        product = await self.products_repo.create_product(product_dict)
        # product_dict["id"] = str(product_id)
        
        return product