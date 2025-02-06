from fastapi import Depends, HTTPException, status, Response
from app.services.cart_service import CartService
from app.models.schemas.cart_schema import CartCreate
from app.models.schemas.response_schema import BaseResponse
from app.models.schemas.user_schema import UserLogin

class CartUseCase:
    def __init__(self, cart_service: CartService = Depends(CartService)):
        self.cart_service = cart_service

    async def add_cart(self, cart_data: CartCreate, user_id) -> BaseResponse:
        result = await self.cart_service.add_cart(cart_data, user_id)
        return result