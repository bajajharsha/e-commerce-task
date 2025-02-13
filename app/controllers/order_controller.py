from fastapi import Depends

from app.usecases.order_usecase import OrderUseCase


class OrderController:
    def __init__(self, order_usecase: OrderUseCase = Depends()):
        self.order_usecase = order_usecase

    async def place_order(self, user_id: str):
        return await self.order_usecase.place_order(user_id)
