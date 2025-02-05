from fastapi import Depends
from passlib.context import CryptContext
from app.repositories.user_repository import UserRepository
from app.models.schemas.user_schema import UserCreate
from app.models.schemas.response_schema import BaseResponse 
from app.utils.security import get_password_hash, create_access_token

class AuthService:
    def __init__(self, user_repo: UserRepository = Depends(UserRepository)):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.user_repo = user_repo

    async def register_user(self, user_data: UserCreate) -> BaseResponse:  # Return BaseResponse instead of UserResponse
        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            return BaseResponse(
                data=None,
                message="User already exists",
                code=400,  # Use a 400 code for error cases
                error="User with this email already exists"
            )

        hashed_password = get_password_hash(user_data.password)
        
        
        user_dict = user_data.dict()
        user_dict["password_hash"] = hashed_password
        
        
        del user_dict["password"]

        user_id = await self.user_repo.create_user(user_dict)
        
        # access_token = create_access_token(data={"sub": str(user_id), "role": user_data.role})
        
        # # Set access token in a secure HttpOnly cookie
        # response.set_cookie(
        #     key="access_token",
        #     value=access_token,
        #     httponly=True,  # Make sure JavaScript cannot access it
        #     secure=False,    # Use only HTTPS in production
        # )

        return BaseResponse(
            data={  # This is now directly returned inside the `data` field of BaseResponse
                "id": str(user_id),  # Use correct dictionary syntax
                "name": user_data.name,
                "email": user_data.email,
                "role": user_data.role,
                # "access_token": access_token
            },
            message="User registered successfully",
            code=200,
            error=None
        )


