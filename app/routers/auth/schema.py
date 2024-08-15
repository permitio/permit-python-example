
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

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


# UserCreate Schema
class PermitUserCreate(BaseModel):
    key: str  # Required, string
    email: Optional[EmailStr]  # Optional, valid email
    first_name: Optional[str]  # Optional, string
    last_name: Optional[str]  # Optional, string
    attributes: Optional[Dict[str, Any]] = {}  # Optional, dictionary with string keys and any values

# RoleAssignmentCreate Schema
class PermitRoleAssignmentCreate(BaseModel):
    role: str  # Required, string
    tenant: Optional[str]  # Optional, string
    resource_instance: Optional[str]  # Optional, string
    user: str  # Required, string

# RoleAssignmentRead Schema
class PermitRoleAssignmentRead(BaseModel):
    id: UUID  # Required, UUID
    user: str  # Required, string
    role: str  # Required, string
    tenant: Optional[str]  # Optional, string
    resource: Optional[str]  # Optional, string
    resource_instance: Optional[str]  # Optional, string
    resource_id: Optional[UUID]  # Optional, UUID
    resource_instance_id: Optional[UUID]  # Optional, UUID
    user_id: UUID  # Required, UUID
    role_id: UUID  # Required, UUID
    tenant_id: UUID  # Required, UUID
    organization_id: UUID  # Required, UUID
    project_id: UUID  # Required, UUID
    environment_id: UUID  # Required, UUID
    created_at: datetime  # Required, datetime
