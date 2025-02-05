from pydantic import BaseModel
from typing import Any, Optional

class BaseResponse(BaseModel):
    data: Optional[Any] = None
    message: str
    code: int
    error: Optional[str] = None
