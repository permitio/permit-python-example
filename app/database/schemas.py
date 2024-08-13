from typing import List, Optional
from pydantic import BaseModel, EmailStr


##### User Schema #####

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    class Config:
        from_attributes = True

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class UserSignInResponse(BaseModel):
    email: EmailStr
    token: str


##### Design Schema #####

class DesignBase(BaseModel):
    title: str
    description: str

class DesignCreate(DesignBase):
    user_email: EmailStr

class DesignDelete(BaseModel): 
    id: int

class DesignEdit(DesignBase):
    id: int

# Properties to return via API
class DesignView(DesignBase):
    id: int
    user_email: str
    comments: Optional[List[str]] = []  

    class Config:
        from_attributes = True 


##### COMMENT SCHEMA #####

class CommentBase(BaseModel):
    id: int

class CommentCreate(BaseModel):
    content: str
    design_id: int
    user_email: int

class CommentDelete(CommentBase):
    pass

class CommentEdit(CommentBase):
    content: str

class CommentView(CommentBase):
    content: str
    design_id: int
    user_email: str





    

