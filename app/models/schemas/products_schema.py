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