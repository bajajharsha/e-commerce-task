from typing import Literal

from bson import ObjectId
from pydantic import BaseModel


class Complaint(BaseModel):
    user_id: ObjectId
    order_id: ObjectId  # Static for now
    product_id: ObjectId  # String for product ID
    issue: str
    image_url: str
    status: Literal["open", "rejected"] = "open"
