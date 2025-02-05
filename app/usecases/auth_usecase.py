from fastapi import Depends, HTTPException
from app.services.auth_services import AuthService
from app.models.schemas.user_schema import UserCreate, UserResponse
from app.models.schemas.response_schema import BaseResponse

class AuthUseCase:
    def __init__(self, auth_service: AuthService = Depends(AuthService)):
        self.auth_service = auth_service

    async def register_user(self, user_data: UserCreate) -> BaseResponse:
        result = await self.auth_service.register_user(user_data)
        if isinstance(result, dict) and "error" in result:
            return BaseResponse(
                data=None,
                message="Registration failed",
                code=400,
                error=result["error"]
            )
        return result