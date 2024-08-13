
from fastapi import Depends
from fastapi.security import HTTPBearer
from .database.database import SessionLocal


token_auth_scheme = HTTPBearer()


async def authenticate(token: str = Depends(token_auth_scheme)):
    return token

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
