
from fastapi import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db_session

token_auth_scheme = HTTPBearer()

async def authenticate(token: str = Depends(token_auth_scheme)):
    return token


DBSessionDep = Depends(get_db_session)
