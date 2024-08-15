from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import DBSessionDep, authenticate
from app.database import models, crud
from app.permit.permit_api import permit
from app.routers.comments.schemas import CommentCreate, CommentDelete, CommentEdit, CommentView

router = APIRouter(
    prefix="/comment",
    tags=["comment"]
)

RESOURCE_NAME = 'comment'


## Create Comment ##
@router.post("", dependencies=[Depends(authenticate)])
async def create_comment(comment: CommentCreate, db: Any = DBSessionDep):
    
    allowed = await permit.check('m', 'create' , RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_comment = db.query(models.Comment).filter(
        models.Comment.user_email == comment.user_email,
        models.Comment.design_id == comment.design_id,
        models.Comment.content == comment.content
    ).first()

    if db_comment:
        raise HTTPException(status_code=400, detail="Comment already exists")

    return crud.create_comment(db, comment)

## Delete Comment ##
@router.delete("/{comment_id}", dependencies=[Depends(authenticate)], response_model=int)
async def delete_comment(comment: CommentDelete, db: Any = DBSessionDep):

    allowed = await permit.check('m', 'delete', RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment.id).first()
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    deleted_comment = await crud.delete_comment(db, comment)

    return comment.id

## Edit Comment ##
@router.patch("/{comment_id}", dependencies=[Depends(authenticate)])
async def edit_comment(comment: CommentEdit, db: Any = DBSessionDep):

    allowed = await permit.check('m', 'edit', RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment.id).first()
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    updated_comment = await crud.update_comment(db, comment)

    return updated_comment

## View Comment ##
@router.get("/{comment_id}", response_model = CommentView, dependencies=[Depends(authenticate)])
async def view_comment(comment_id: int, db: Any = DBSessionDep):

    allowed = await permit.check('m', 'view', RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return db_comment
