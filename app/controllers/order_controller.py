from fastapi import Depends, Response
from app.models.schemas.cart_schema import CartCreate
from app.models.schemas.response_schema import BaseResponse
from app.usecases.order_usecase import OrderUseCase

class OrderController:
    def __init__(self, order_usecase: OrderUseCase = Depends()):
        self.order_usecase = order_usecase

    async def place_order(self, user_id: str):
        return await self.order_usecase.place_order(user_id)