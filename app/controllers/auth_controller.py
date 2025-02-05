from fastapi import Depends
from app.usecases.auth_usecase import AuthUseCase
from app.models.schemas.user_schema import UserCreate, UserResponse
from app.models.schemas.response_schema import BaseResponse

class AuthController:
    def __init__(self, auth_usecase: AuthUseCase = Depends(AuthUseCase)):
        self.auth_usecase = auth_usecase

    async def register(self, user: UserCreate) -> BaseResponse:
        return await self.auth_usecase.register_user(user)
