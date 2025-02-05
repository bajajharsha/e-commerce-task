from pydantic import BaseModel
from typing import List
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
    seller_id: ObjectId  # Associate with seller's ID
