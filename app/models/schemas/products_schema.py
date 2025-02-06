from fastapi import Form
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

class ProductCreate(BaseModel):
    title: str
    description: str
    category: str
    price: float
    rating: float
    brand: str
    images: List[str]
    thumbnail: str
    seller_id: str


class ProductUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    brand: Optional[str] = None
    images: Optional[List[str]] = None
    thumbnail: Optional[str] = None
    seller_id: Optional[str] = None
    created_at: Optional[str] = None
    
class ProductCreateSchema(BaseModel):
    title: str
    description: str
    category: str
    price: float
    rating: Optional[float] = None
    brand: Optional[str] = None
    thumbnail: Optional[str] = None

async def parse_form(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    price: float = Form(...),
    rating: Optional[float] = Form(None),
    brand: Optional[str] = Form(None),
    thumbnail: Optional[str] = Form(None),
):
    return ProductCreateSchema(
        title=title,
        description=description,
        category=category,
        price=price,
        rating=rating,
        brand=brand,
        thumbnail=thumbnail
    )
# class ProductResponse(BaseModel):
#     id: str
#     title: str
#     description: str
#     category: str
#     price: float
#     images: List[str]
#     rating: Optional[float] = None
#     brand: Optional[str] = None
#     thumbnail: Optional[str] = None
#     seller_id: str