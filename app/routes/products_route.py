# app/routes/products_route.py
from fastapi import APIRouter, Depends, status, UploadFile, File
from app.controllers.products_controller import ProductsController
from app.models.schemas.response_schema import BaseResponse
from app.utils.dependencies import RoleChecker
from app.models.schemas.products_schema import ProductUpdateSchema, ProductCreateSchema, parse_form

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=BaseResponse)
async def get_products(products_controller: ProductsController = Depends()) -> BaseResponse:
    return await products_controller.get_products()

    
@router.get("/preload-products", response_model=BaseResponse)
async def preload_products(products_controller: ProductsController = Depends()) -> BaseResponse:
    return await products_controller.preload_products()

 
@router.get("/{product_id}", response_model=BaseResponse)
async def get_product_by_id(product_id: str, products_controller: ProductsController = Depends()) -> BaseResponse:
    return await products_controller.get_product_by_id(product_id)

@router.put("/{product_id}", response_model=BaseResponse, dependencies=[Depends(RoleChecker(["admin", "seller"]))])
async def update_product(
    product_id: str,
    product_data: ProductUpdateSchema,
    product_controller: ProductsController = Depends(),
) -> BaseResponse:
    return await product_controller.update_product(product_id, product_data)

@router.post("/", response_model=BaseResponse, dependencies=[Depends(RoleChecker(["admin", "seller"]))])
async def add_product(
    product_data: ProductCreateSchema = Depends(parse_form),
    image: UploadFile = File(...),
    product_controller: ProductsController = Depends()
) -> BaseResponse:
    return await product_controller.add_product(product_data, image)
