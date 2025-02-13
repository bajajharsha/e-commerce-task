from typing import Optional

from pydantic import BaseModel


class ComplaintCreate(BaseModel):
    issue: str
    order_id: str
    product_id: str
    image_url: Optional[str] = None

    # user_id: ObjectId
    # order_id: ObjectId
    # product_id: ObjectId
    # issue: str
    # image_url: str
    # status: Literal["open", "rejected"]
