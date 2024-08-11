from fastapi import APIRouter, Depends

from app.permit_dependency import check_feed_permission

router = APIRouter()

# Feed Snake RBAC example
@router.get("/feed-snake")
async def feed_snake(user_id: str, permitted: bool = Depends(check_feed_permission)):
    return {"message": f"User {user_id} is feeding the snake!"}
    

# Count


