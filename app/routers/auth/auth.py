import base64
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from app.database.database import get_db_session
from app.permit.permit_api import sync_user, assign_role
from app.database import crud
from app.routers.auth.schema import  UserSignInRequest, UserSignInResponse, UserBase, UserCreateRequest
from permit.api.models import RoleAssignmentCreate, UserCreate, RoleAssignmentRead
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/signup",tags=["signup"], response_model= UserBase)
async def create_user_route(user: UserCreateRequest, db_session = Depends(get_db_session)):
    db_user = await crud.get_user(db_session, user)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Prepare data for syncing with permit API
    user_data: UserCreate = {
        "key": user.email,
        "email": user.email,
        "first_name": user.name,
        "last_name": '-',
        "attributes": {},
    }
    
    # Sync user with permit API
    synced_user = await sync_user(user_data)

    user = await crud.create_user(db_session=db_session, user=user)

    created_user = UserBase(
    email=user.email,
    name=user.name
   )

    return created_user

@router.post("/signin",tags=["signin"], response_model=UserSignInResponse)
async def sign_in(user: UserSignInRequest,  db_session = Depends(get_db_session)):
    db_user = await crud.get_user(db_session, user)

    decoded_password = base64.b64decode(db_user.hash_pwd).decode('utf-8')

    if not db_user or not decoded_password == user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = UserSignInResponse(
    access_token="fake-jwt-token-for-demo"
   )

    return token

@router.post('/assign-role', tags=['assign-role'], response_model=RoleAssignmentRead)
async def assigned_role_to_user(assignedRoleData: RoleAssignmentCreate):
  
    roleAssigned: RoleAssignmentRead = await assign_role(assignedRoleData)

    return roleAssigned
