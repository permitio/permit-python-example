from permit import Permit
from permit.api.models import RoleAssignmentCreate, UserCreate, UserRead, RoleAssignmentRead
from app.config import settings


# This line initializes the SDK and connects your python app
# to the Permit.io PDP container you've set up.
permit = Permit(
    # your secret API KEY
    token=settings.permit_api_key,

    # in production, you might need to change this url to fit your deployment
    # this is the address where you can find the PDP container.
    pdp="http://permit_pdp:7000",
    
    # optional, the timeout in seconds for the request to the PDP container (supported from version 2.5.0)
    pdp_timeout=5,
    # optional, the timeout in seconds for the request to Permit cloud API (supported from version 2.5.0)
    api_timeout=5,
)

async def sync_user(data: UserCreate) -> UserRead:
  
    synced_user = await permit.api.users.sync(data)
    return synced_user

async def assign_role(data: RoleAssignmentCreate) -> RoleAssignmentRead:

    
    assigned_role = await permit.api.users.assign_role(
        {
        "user": data.user,
        "role": data.role,
        "tenant": 'default'
       })

    return assigned_role




