from fastapi import HTTPException, status
from permit import UserRead, Permit
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


async def sync_user(data: Dict[str, Any]) -> dict:
    # Validate the input data
    validated_data = UserSyncData(**data)

    # Perform the sync operation
    await permit.api.users.sync(
        {
            "key": validated_data.key,
            "email": validated_data.email,
            "first_name": validated_data.first_name,
            "last_name": validated_data.last_name,
            "attributes": validated_data.attributes,
        }
    )
    return {"message": f"User {validated_data.email} Sync To Permit Successfuly."}

async def assign_role(data: Dict[str,Any]):
    #Validate the input data
    validated_data = AssignRoleData(**data)

    await permit.api.users.assign_role({"role": validated_data.role, "user": validated_data.user })

    return {"message": f"User {validated_data.user} assign to role {validated_data.role} Successfuly."}


