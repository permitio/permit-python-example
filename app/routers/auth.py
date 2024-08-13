from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.permit.permit_api import sync_user, assign_role
from app.permit.schemas import AssignRoleData, UserSyncData
from ..database import schemas, models, crud
from ..dependencies import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/signup/",tags=["signup"], response_model=schemas.User)
async def create_user_route(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Prepare data for syncing with permit API
    user_data: dict = {
        "key": 'user|892179821739812389327',
        "email": 'jhonCohen@gmail.com',
        "first_name": 'john',
        "last_name": 'cohen',
        "attributes": {},
    }
    
    # Sync user with permit API
    await sync_user(user_data)

    return crud.create_user(db=db, user=user)

@router.post("/signin",tags=["signin"], response_model=schemas.UserSignInResponse)
def sign_in(user: schemas.UserSignIn, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not db_user.hash_pwd == user.password + "notreallyhashed":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate a fake JWT token for demonstration
    fake_jwt_token = "fake-jwt-token-for-demo"
    
    return {"email": db_user.email, "token": fake_jwt_token}

@router.post('/assign-role', tags=['assign-role'], response_model=Any)
async def assigned_role_to_user(assignedRoleData: AssignRoleData):
    print ("hellok")

     # Prepare data for syncing with permit API
    assigned_role_data : dict = {
        "user": assignedRoleData.user,
        "role": assignedRoleData.role
    }

    roleAssigned = await assign_role(assigned_role_data)

    return roleAssigned