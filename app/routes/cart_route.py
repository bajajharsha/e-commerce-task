# routes/auth_routes.py
from fastapi import APIRouter, Depends, Response
from app.utils.dependencies import RoleChecker
from app.models.schemas.cart_schema import CartCreate
from app.utils.auth import get_current_user
from app.controllers.cart_controller import CartController

router = APIRouter(prefix="/cart", tags=["Authentication"])

@router.post("/add", dependencies=[Depends(RoleChecker(["admin"]))])
async def register(
    cart_items: CartCreate, 
    user_id = Depends(get_current_user),
    cart_controller: CartController = Depends()):
    return await cart_controller.add_cart(cart_items, user_id)
