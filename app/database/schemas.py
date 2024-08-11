from pydantic import BaseModel, EmailStr

from app.database.models import SnakeType

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    class Config:
        orm_mode = True

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class UserSignInResponse(BaseModel):
    email: EmailStr
    token: str

