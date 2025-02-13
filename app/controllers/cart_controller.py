from fastapi import Depends

from app.models.schemas.cart_schema import CartCreate
from app.usecases.cart_usecase import CartUseCase


class CartController:
    def __init__(self, cart_usecase: CartUseCase = Depends()):
        self.cart_usecase = cart_usecase

    async def add_cart(self, cart: CartCreate, user_id: str):
        return await self.cart_usecase.add_cart(cart, user_id)

    async def get_cart(self, user_id: str):
        return await self.cart_usecase.get_cart(user_id)
