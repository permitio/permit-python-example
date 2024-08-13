from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from ..database import schemas, models, crud

router = APIRouter()

## Create Comment ##
@router.post("/create-comment")
async def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(
        models.Comment.user_email == comment.user_email,
        models.Comment.design_id == comment.design_id,
        models.Comment.content == comment.content
    ).first()

    if db_comment:
        raise HTTPException(status_code=400, detail="Comment already exists")

    return crud.create_comment(db, comment)

## Delete Comment ##
@router.delete("/delete-comment")
async def delete_comment(comment: schemas.CommentDelete, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment.id).first()
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    crud.delete_comment(db, comment)
    return {"message": "Comment deleted successfully"}

## Edit Comment ##
@router.patch("/edit-comment")
async def edit_comment(comment: schemas.CommentEdit, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment.id).first()
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return crud.update_comment(db, comment)

## View Comment ##
@router.get("/view-comment/{comment_id}", response_model=schemas.CommentView)
async def view_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return db_comment
