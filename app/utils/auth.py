from fastapi import HTTPException, Request, status
from jose import JWTError, jwt

from app.config.settings import settings

# from models.domain.user import User
# from app.utils.auth import SECRET_KEY, ALGORITHM


async def get_current_user(request: Request):
    # Extract the JWT token from the cookies
    token = request.cookies.get("access_token")

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT token is missing from cookies",
        )

    try:
        # Decode the token and extract the user data
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        return user_id

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
        )
