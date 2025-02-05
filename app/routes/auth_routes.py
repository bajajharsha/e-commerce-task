# routes/auth_routes.py
from fastapi import APIRouter, Depends
from app.controllers.auth_controller import AuthController
from app.models.schemas.user_schema import UserCreate, UserResponse
from app.models.schemas.response_schema import BaseResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=BaseResponse)
async def register(user: UserCreate, auth_controller: AuthController = Depends(AuthController)):
    return await auth_controller.register(user)
