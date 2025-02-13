# app/usecases/products_usecase.py
from fastapi import Depends, HTTPException, UploadFile

from app.models.schemas.products_schema import ProductCreateSchema
from app.services.products_service import ProductsService


class ProductsUseCase:
    def __init__(self, products_service: ProductsService = Depends()):
        self.products_service = products_service

    async def get_products(self):
        return await self.products_service.get_products()

    async def preload_products(self):
        return await self.products_service.preload_products()

    async def get_product_by_id(self, product_id):
        return await self.products_service.get_product_by_id(product_id)

    async def update_product(self, product_id, product_data):
        return await self.products_service.update_product(product_id, product_data)

    async def add_product(
        self, product_data: ProductCreateSchema, image: UploadFile, seller_id
    ):
        if not image.content_type.startswith("image/"):
            raise HTTPException(400, "File must be an image")
        return await self.products_service.create_product(
            product_data, image, seller_id
        )
