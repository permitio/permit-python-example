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

class SnakeBase(BaseModel):
    id: int

class SnakeCreate(SnakeBase):
    type: SnakeType
    tank_id: int

class Snake(SnakeBase):
    id: int

    class Config:
        orm_mode = True

class TankBase(BaseModel):
    pass

class TankCreate(TankBase):
    pass

class Tank(TankBase):
    id: int
    snakes: list[Snake] = []

    class Config:
        orm_mode = True