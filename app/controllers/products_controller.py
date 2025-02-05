# app/controllers/products_controller.py
from fastapi import Depends, HTTPException, status
from app.usecases.products_usecase import ProductsUseCase
from fastapi.responses import JSONResponse
from app.models.schemas.response_schema import BaseResponse
from app.models.schemas.products_schema import ProductUpdateSchema

class ProductsController:
    def __init__(self, products_usecase: ProductsUseCase = Depends()):
        self.products_usecase = products_usecase

    async def get_products(self) -> BaseResponse:
        try:
            return await self.products_usecase.get_products()
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "message": "Error while fetching the products",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "error": str(e)
                }
            )

    async def preload_products(self) -> BaseResponse:
        try:
            return await self.products_usecase.preload_products()
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "message": "Error while preloading products",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "error": str(e)
                }
            )
            
    async def get_product_by_id(self, product_id: str, products_usecase: ProductsUseCase = Depends()) -> BaseResponse:
        try:
            product = await self.products_usecase.get_product_by_id(product_id)
            if not product:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=BaseResponse(
                        data=None,
                        message="Some error occurred while fetching the data",
                        code=status.HTTP_404_NOT_FOUND,
                        error="Not Found"
                    )
                )
            
            return product
        except Exception as e:
            return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=BaseResponse(
                        data=None,
                        message="Some error occurred while fetching the data",
                        code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        error=str(e)
                    )
            )
            
    async def update_product(self, product_id: str, product_data: ProductUpdateSchema):
        # Call the service to update the product
        updated_product = await self.products_usecase.update_product(product_id, product_data)
        if not updated_product:
            return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=BaseResponse(
                        data=None,
                        message="Some error occurred while fetching the data",
                        code=status.HTTP_404_NOT_FOUND,
                        error="Product Not Found"
                    )
            )
        return updated_product