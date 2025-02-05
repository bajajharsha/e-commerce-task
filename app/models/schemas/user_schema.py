from typing import Literal
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["admin", "buyer", "seller"]

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: Literal["admin", "buyer", "seller"]