from fastapi import Depends, Response, status
from fastapi.responses import JSONResponse  # This allows you to specify status codes
from passlib.context import CryptContext

from app.models.domain.user import User
from app.models.schemas.response_schema import BaseResponse
from app.models.schemas.user_schema import UserCreate, UserLogin
from app.repositories.user_repository import UserRepository
from app.utils.security import create_access_token, get_password_hash, verify_password


class AuthService:
    def __init__(self, user_repo: UserRepository = Depends(UserRepository)):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.user_repo = user_repo

    async def register_user(
        self, user_data: UserCreate
    ) -> BaseResponse:  # Return BaseResponse instead of UserResponse
        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            return JSONResponse(
                content=BaseResponse(
                    data=None,
                    message="User already exists",
                    code=status.HTTP_400_BAD_REQUEST,
                    error="User with this email already exists",
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        hashed_password = get_password_hash(user_data.password)

        user_dict = user_data.dict()
        user_dict["password_hash"] = hashed_password

        del user_dict["password"]

        user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password,
            role=user_data.role,
        )

        user_dict = user.to_dict()

        user_id = await self.user_repo.create_user(user_dict)

        return JSONResponse(
            content=BaseResponse(
                data={  # This is now directly returned inside the `data` field of BaseResponse
                    "id": str(user_id),  # Use correct dictionary syntax
                    "name": user_data.name,
                    "email": user_data.email,
                    "role": user_data.role,
                    # "access_token": access_token
                },
                message="User registered successfully",
                code=status.HTTP_201_CREATED,
                error=None,
            ).model_dump(),
            status_code=status.HTTP_201_CREATED,
        )

    async def login_user(
        self, user_data: UserLogin, response: Response
    ) -> BaseResponse:
        user = await self.user_repo.get_user_by_email(user_data.email)
        if not user:
            return JSONResponse(
                content=BaseResponse(
                    data=None,
                    message="User does not exists",
                    code=status.HTTP_400_BAD_REQUEST,
                    error="User with this email does not exist.",
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Verify password
        if not verify_password(user_data.password, user["password_hash"]):
            return JSONResponse(
                content=BaseResponse(
                    data=None,
                    message="User does not exists",
                    code=status.HTTP_401_UNAUTHORIZED,
                    error="Invalid credentials",
                ).model_dump(),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        # Create JWT Token
        access_token = create_access_token(
            data={"sub": str(user["_id"]), "role": user["role"]}
        )

        # Set the JWT token in an HttpOnly cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,  # Make sure JavaScript cannot access it
            secure=False,  # Set to True for production (HTTPS only)
        )

        return BaseResponse(
            data={"message": "Login successful", "access_token": access_token},
            message="Login successful",
            code=status.HTTP_200_OK,
            error=None,
        )
