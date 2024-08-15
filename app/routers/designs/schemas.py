from typing import List, Optional
from pydantic import BaseModel, EmailStr


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

class DesignDeleteResponse(BaseModel):
    id: int

class DesignEditResponse(BaseModel):
    id: int
