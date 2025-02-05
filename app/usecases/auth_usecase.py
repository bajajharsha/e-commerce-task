from fastapi import Depends, HTTPException, status, Response
from app.services.auth_services import AuthService
from app.models.schemas.user_schema import UserCreate, UserResponse
from app.models.schemas.response_schema import BaseResponse
from app.models.schemas.user_schema import UserLogin

class AuthUseCase:
    def __init__(self, auth_service: AuthService = Depends(AuthService)):
        self.auth_service = auth_service

    async def register_user(self, user_data: UserCreate) -> BaseResponse:
        result = await self.auth_service.register_user(user_data)
        if isinstance(result, dict) and "error" in result:
            return BaseResponse(
                data=None,
                message="Registration failed",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=result["error"]
            )
        return result
    
    
    async def login_user(self, user_data: UserLogin, response: Response) -> BaseResponse:
        return await self.auth_service.login_user(user_data, response)