from typing import List
from bson import ObjectId
from datetime import datetime

class Product:
    def __init__(self, title: str, description: str, category: str, price: float, 
                 rating: float, brand: str, images: List[str], thumbnail: str, 
                 seller_id: ObjectId):
        self._id = ObjectId()  # Unique ObjectId for the product
        self.title = title
        self.description = description
        self.category = category
        self.price = price
        self.rating = rating
        self.brand = brand
        self.images = images  # List of image URLs
        self.thumbnail = thumbnail  # Thumbnail URL
        self.seller_id = seller_id  # Reference to the seller's user ID
        self.created_at = datetime.utcnow()  # Timestamp for when the product was created

    def to_dict(self):
        return {
        "_id": str(self._id),  # Convert ObjectId to string
        "title": self.title,
        "description": self.description,
        "category": self.category,
        "price": self.price,
        "seller_id": str(self.seller_id),  # Convert seller_id ObjectId to string
        "images": self.images,
        "thumbnail": self.thumbnail,
        "rating": self.rating,
        "brand": self.brand,
        "created_at": self.created_at.isoformat() if self.created_at else None
    }
