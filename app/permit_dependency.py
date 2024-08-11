from fastapi import HTTPException, status
from permit import Permit

# This line initializes the SDK and connects your python app
# to the Permit.io PDP container you've set up.
permit = Permit(
    # your secret API KEY
    token="permit_key_71I3vy7vb8XevK0WB25jg3ZtnItdE6Gtk6yZwC1VTH9QQlZeulAwE4Wfpa0bH9nRAfOMjsrw8PoiiR7PmeQEpK",

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