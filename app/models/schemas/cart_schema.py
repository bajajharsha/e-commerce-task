from typing import Literal
from pydantic import BaseModel, EmailStr

class CartCreate(BaseModel):
    # user_id: ObjectId
    product_id: str
    quantity: int