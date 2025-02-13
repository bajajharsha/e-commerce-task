from typing import List

from pydantic import BaseModel


class CartCreate(BaseModel):
    # user_id: ObjectId
    product_id: str
    quantity: int


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types like ObjectId


class Order(BaseModel):
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: str  # You can use a Literal if needed

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types like ObjectId
