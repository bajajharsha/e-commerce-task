# routes/auth_routes.py
from fastapi import APIRouter, Depends, Response
from app.utils.dependencies import RoleChecker
from app.utils.auth import get_current_user
from app.controllers.order_controller import OrderController

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", dependencies=[Depends(RoleChecker(["admin", "Buyer"]))])
async def place_order(
    user_id = Depends(get_current_user),
    order_controller: OrderController = Depends()
):
    return await order_controller.place_order(user_id)
