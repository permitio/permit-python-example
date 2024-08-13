
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer

from app import permit

token_auth_scheme = HTTPBearer()


async def permit_authorize(request: Request, token: str = Depends(token_auth_scheme), body={}):
    resource_name = request.url.path.strip('/').split('/')[0]
    method = request.method.lower()
    resource = await request.json() if method in ["post", "put"] else body
    user = token.credentials

    allowed = await permit.check(user, method, {
        "type": resource_name,
        "attributes": resource
    })

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized")