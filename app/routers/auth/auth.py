import base64
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from app.database.database import get_db_session
from app.permit.permit_api import sync_user, assign_role
from app.database import crud
from app.routers.auth.schema import PermitRoleAssignmentCreate, PermitRoleAssignmentRead, PermitUserCreate, UserSignInRequest, UserSignInResponse, UserBase, UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/signup",tags=["signup"], response_model= UserBase)
async def create_user_route(user: UserCreate, db_session = Depends(get_db_session)):
    db_user = await crud.get_user(db_session, user)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Prepare data for syncing with permit API
    user_data: PermitUserCreate = {
        "key": user.email,
        "email": user.email,
        "first_name": user.name,
        "last_name": '-',
        "attributes": {},
    }
    
    # Sync user with permit API
    await sync_user(user_data)

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

@router.post('/assign-role', tags=['assign-role'], response_model=PermitRoleAssignmentRead)
async def assigned_role_to_user(assignedRoleData: PermitRoleAssignmentCreate):
  
     # Prepare data for syncing with permit API
    assigned_role_data : PermitRoleAssignmentCreate = {
        "user": assignedRoleData.user,
        "role": assignedRoleData.role
    }

    roleAssigned = await assign_role(assigned_role_data)

    return PermitRoleAssignmentCreate(roleAssigned)
