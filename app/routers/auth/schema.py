
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

##### User Schema #####

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreateRequest(UserBase):
    password: str

class User(UserBase):
    class Config:
        from_attributes = True

class UserSignInRequest(BaseModel):
    email: EmailStr
    password: str


class UserSignInResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

