
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi import Depends

from app.database.database import get_db_session

token_auth_scheme = HTTPBearer()

async def authenticate(token: str = Depends(token_auth_scheme)) -> str:
    return token.credentials


DBSessionDep = Depends(get_db_session)
