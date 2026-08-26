from pydantic import BaseModel
from pydantic import ConfigDict, EmailStr, StringConstraints
from typing import Annotated


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8, max_length=72)]


class UserOut(BaseModel):
    username: str
    email: EmailStr
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    email: EmailStr


class UserPassword(BaseModel):
    current_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
