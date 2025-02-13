from fastapi import Depends

from app.models.schemas.cart_schema import CartCreate
from app.models.schemas.response_schema import BaseResponse
from app.services.cart_service import CartService


class CartUseCase:
    def __init__(self, cart_service: CartService = Depends(CartService)):
        self.cart_service = cart_service

    async def add_cart(self, cart_data: CartCreate, user_id) -> BaseResponse:
        result = await self.cart_service.add_cart(cart_data, user_id)
        return result

    async def get_cart(self, user_id: str):
        return await self.cart_service.get_cart(user_id)
