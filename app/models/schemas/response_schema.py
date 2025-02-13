from typing import Any, Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    data: Optional[Any] = None
    message: str
    code: int
    error: Optional[str] = None
