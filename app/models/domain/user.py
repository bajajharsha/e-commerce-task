from typing import Literal
from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    name: str
    email: EmailStr
    password_hash: str
    role: Literal["admin", "buyer", "seller"]

