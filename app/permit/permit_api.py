from fastapi import HTTPException, status
from permit import Permit
from typing import Any, Dict
import os

from dotenv import load_dotenv

load_dotenv()

from app.permit.schemas import AssignRoleData, UserSyncData

api_key = os.getenv("PERMIT_API_KEY")

if api_key is None:
    raise ValueError("No API_KEY environment variable set!")

# This line initializes the SDK and connects your python app
# to the Permit.io PDP container you've set up.
permit = Permit(
    # your secret API KEY
    token=api_key,

    # in production, you might need to change this url to fit your deployment
    # this is the address where you can find the PDP container.
    pdp="http://localhost:7766",
    
    # optional, the timeout in seconds for the request to the PDP container (supported from version 2.5.0)
    pdp_timeout=5,
    # optional, the timeout in seconds for the request to Permit cloud API (supported from version 2.5.0)
    api_timeout=5,
)

from typing import Optional, Dict, Any

async def check_permission(
    user_key: str,
    action: str,
    resource_type: str,
    tenant: Optional[str]  = 'default', 
    user_attributes: Optional[Dict[str, Any]] = None,
    resource_attributes: Optional[Dict[str, Any]] = None
) -> Any:
    # Construct the user dictionary, including attributes only if provided
    user_dict = {"key": user_key}
    if user_attributes:
        user_dict["attributes"] = user_attributes

    # Construct the resource dictionary, including attributes only if provided
    resource_dict = {
        "type": resource_type,
        "attributes": {
            "author": user_key,
        },
        "tenant": tenant,
    }
    if resource_attributes:
        resource_dict["attributes"] = resource_attributes

    # Call the permit check function with the constructed dictionaries
    return await permit.check(user_key, action, resource_dict)



async def sync_user(data: Dict[str, Any]) -> dict:
    # Validate the input data
    validated_data = UserSyncData(**data)

    # Perform the sync operation
    synced_user = await permit.api.users.sync(
        {
            "key": validated_data.key,
            "email": validated_data.email,
            "first_name": validated_data.first_name,
            "last_name": validated_data.last_name,
            "attributes": validated_data.attributes,
        }
    )
    return synced_user

async def assign_role(data: Dict[str,Any]):
    #Validate the input data
    validated_data = AssignRoleData(**data)

    assigned_role = await permit.api.users.assign_role({"role": validated_data.role, "user": validated_data.user, "tenant": 'default' })

    return assigned_role




