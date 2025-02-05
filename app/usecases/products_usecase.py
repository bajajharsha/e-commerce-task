# app/usecases/products_usecase.py
from fastapi import Depends
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
