
from fastapi import APIRouter, Depends, HTTPException
from app.database.database import get_db_session
from app.dependencies import authenticate
from app.database import crud
from app.database.models import Comment
from app.permit.permit_api import permit
from app.routers.comments.schemas import CommentDelete, CommentEdit, CommentView
from sqlalchemy.future import select
from fastapi import status


router = APIRouter(
    prefix="/comment",
    tags=["comment"]
)

RESOURCE_NAME = 'comment'

## Create Comment ##
@router.post("", dependencies=[Depends(authenticate)], response_model=Comment)
async def create_comment(comment: Comment, db_session = Depends(get_db_session)):
    
    allowed = await permit.check(comment.user_email, 'create' , RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    db_comment = (await db_session.execute(
    select(Comment).where(
        Comment.user_email == comment.user_email,
        Comment.design_id == comment.design_id,
        Comment.content == comment.content
    ))).scalars().first()


    if db_comment:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment already exists")

    created_comment = await crud.create_comment(db_session, comment)

    return Comment(
        content=created_comment.content,
        design_id=created_comment.design_id,
        user_email=created_comment.user_email
    )

## Delete Comment ##
@router.delete("/{comment_id}", response_model=Comment)
async def delete_comment(comment: CommentDelete, user = Depends(authenticate), db_session = Depends(get_db_session)):

    allowed = await permit.check(user, 'delete', RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    db_comment = db_session.query(Comment).filter(Comment.id == comment.id).first()
    
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    deleted_comment = await crud.delete_comment(db_session, comment)

    return Comment(
        content=deleted_comment.content,
        design_id=deleted_comment.design_id,
        user_email=deleted_comment.user_email
    )


## Edit Comment ##
@router.patch("/{comment_id}")
async def edit_comment(comment: CommentEdit,user = Depends(authenticate), db_session = Depends(get_db_session)):

    allowed = await permit.check(user, 'edit', RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    db_comment = db_session.query(Comment).filter(Comment.id == comment.id).first()
    
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    updated_comment = await crud.update_comment(db_session, comment)

    return updated_comment

## View Comment ##
@router.get("/{comment_id}", response_model = CommentView)
async def view_comment(comment_id: int, user = Depends(authenticate), db_session = Depends(get_db_session)):

    allowed = await permit.check(user, 'view', RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    db_comment = db_session.query(Comment).filter(Comment.id == comment_id).first()
    
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    return db_comment
