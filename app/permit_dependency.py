from fastapi import HTTPException, status
from permit import Permit
import os

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

async def check_feed_permission(user_id: str, resource: str = "snake", action: str = "feed"):
    permitted = await permit.check(user_id, action, resource)
    if not permitted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to feed the snake."
        )
    return permitted