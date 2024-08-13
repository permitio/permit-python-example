from pydantic import BaseModel, EmailStr, Field
from typing import Dict, Any


class UserSyncData(BaseModel):
    key: str
    email: EmailStr
    first_name: str
    last_name:  str
    attributes: Any

class AssignRoleData(BaseModel):
    user: str
    role: str


