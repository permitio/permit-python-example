
import re
from typing import Any, Dict, Optional
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer

from app import permit
from app.permit.permit_api import check_permission

token_auth_scheme = HTTPBearer()

def extract_first_occurrence(input_string: str) -> str:
    # Define the regex pattern to capture text after the first '/'
    pattern = r"/([^/]+)"

    # Search for the first occurrence
    match = re.search(pattern, input_string)

    # Return the matched group or an empty string if no match is found
    return match.group(1) if match else ""

def get_action_method_base(method: str):
    if method == 'POST':
        action = 'create'
    elif method == 'DELETE':
        action = 'delete'
    elif method == 'GET':
        action = 'view'
    elif method == 'PATCH':
        action = 'edit'
    else:
        raise HTTPException(status_code=405, detail="Method Not Allowed")    
    return action

async def permit_authorize(request: Request, token: str = Depends(token_auth_scheme)):
    resource_name = extract_first_occurrence(request.url.path)
   
    action = get_action_method_base(request.method)
  
    user = token.credentials

    allowed = await check_permission(user, action,resource_name)

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized")