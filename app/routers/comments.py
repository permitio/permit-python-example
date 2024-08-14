from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import authenticate, get_db
from app.permit.permit_dependencies import permit_authorize
from ..database import schemas, models, crud

router = APIRouter(
    prefix="/comment",
    tags=["comment"]
)

## Create Comment ##
@router.post("", dependencies=[Depends(authenticate), Depends(permit_authorize)])
async def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    print("hello again")
    db_comment = db.query(models.Comment).filter(
        models.Comment.user_email == comment.user_email,
        models.Comment.design_id == comment.design_id,
        models.Comment.content == comment.content
    ).first()

    if db_comment:
        raise HTTPException(status_code=400, detail="Comment already exists")

    return crud.create_comment(db, comment)

## Delete Comment ##
@router.delete("/{comment_id}", dependencies=[Depends(authenticate), Depends(permit_authorize)])
async def delete_comment(comment: schemas.CommentDelete, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment.id).first()
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    crud.delete_comment(db, comment)
    return comment.id

## Edit Comment ##
@router.patch("/{comment_id}", dependencies=[Depends(authenticate), Depends(permit_authorize)])
async def edit_comment(comment: schemas.CommentEdit, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment.id).first()
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return crud.update_comment(db, comment)

## View Comment ##
@router.get("/{comment_id}", response_model=schemas.CommentView, dependencies=[Depends(authenticate), Depends(permit_authorize)])
async def view_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return db_comment
