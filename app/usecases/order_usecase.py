from fastapi import Depends

from app.services.order_service import OrderService

# from app.models.schemas.cart_schema import CartCreate


class OrderUseCase:
    def __init__(self, order_service: OrderService = Depends()):
        self.order_service = order_service

    async def place_order(self, user_id: str):
        return await self.order_service.place_order(user_id)
