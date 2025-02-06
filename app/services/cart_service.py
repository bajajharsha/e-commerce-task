from fastapi import Depends, status, Response
from app.repositories.cart_repository import CartRepository
from app.models.schemas.cart_schema import CartCreate
from app.models.schemas.response_schema import BaseResponse 
from app.utils.security import get_password_hash, create_access_token, verify_password
from fastapi.responses import JSONResponse  # This allows you to specify status codes
from app.models.schemas.user_schema import UserLogin
from app.models.domain.user import User

class CartService:
    def __init__(self, cart_repo: CartRepository = Depends(CartRepository)):
        self.cart_repo = cart_repo

    async def add_cart(self, cart_data: CartCreate, user_id) -> BaseResponse:  # Return BaseResponse instead of UserResponse
        data = cart_data.dict()
        data["user_id"] = user_id
        
        if data["product_id"] == "" or data["product_id"] == None:
            return JSONResponse(status_code=400, content={"message": "Product ID is required"})
        
        print(data)
        result = await self.cart_repo.add_cart(data)
        data["_id"] = str(result.inserted_id)
        return {
            "status": "success",
            "data": data
        }
        
    async def get_cart(self, user_id: str) -> BaseResponse:
        cart_items = await self.cart_repo.get_cart_by_user_id(user_id)
        if not cart_items:
            return {"status": "error", "message": "No cart items found for the user"}
        return {"status": "success", "data": cart_items, "count": len(cart_items)}
        