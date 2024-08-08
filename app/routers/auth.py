from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import schemas, models, crud
from ..dependencies import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/signup/",tags=["signup"], response_model=schemas.User)
def create_user_route(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/signin",tags=["signin"], response_model=schemas.UserSignInResponse)
def sign_in(user: schemas.UserSignIn, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not db_user.hash_pwd == user.password + "notreallyhashed":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate a fake JWT token for demonstration
    fake_jwt_token = "fake-jwt-token-for-demo"
    
    return {"email": db_user.email, "token": fake_jwt_token}