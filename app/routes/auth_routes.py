# routes/auth_routes.py
from fastapi import APIRouter, Depends, Response

from app.controllers.auth_controller import AuthController
from app.models.schemas.response_schema import BaseResponse
from app.models.schemas.user_schema import UserCreate, UserLogin
from app.utils.dependencies import RoleChecker

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=BaseResponse)
async def register(
    user: UserCreate, auth_controller: AuthController = Depends(AuthController)
):
    return await auth_controller.register(user)


@router.post("/login", response_model=BaseResponse)
async def login(
    user: UserLogin,
    response: Response,
    auth_controller: AuthController = Depends(AuthController),
):
    return await auth_controller.login(user, response)


@router.get("/test")
async def test(payload: dict = Depends(RoleChecker(["seller"]))):
    return "yayayayayaya"
