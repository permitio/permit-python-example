from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas

##### USER CRUD OPERATIONS ####

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hash_pwd=fake_hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

##### DESIGN CRUD OPERATIONS ####

def create_design(db: Session, design: schemas.DesignCreate):
    db_design = models.Design(user_email=design.user_email, title=design.title, description=design.description)
    db.add(db_design)
    db.commit()
    db.refresh(db_design)

    return {"message": "Design created successfully", "design_id": db_design.id}

def delete_design(db: Session, deleteDesign: schemas.DesignDelete):
    design = db.query(models.Design).filter(models.Design.id == deleteDesign.id).first()

    if not design:
        # Handle the case where the design does not exist
        raise HTTPException(status_code=404, detail="Design not found")
    
    db.delete(design)
    db.commit()

    return {"message": "Design deleted successfully", "design_id": design.id}

def edit_design(db: Session, design_id: int, new_title: Optional[str] = None, new_description: Optional[str] = None):
    design = db.query(models.Design).filter(models.Design.id == design_id).first()
    
    if design is None:
        # Raise an exception if the design does not exist
        raise HTTPException(status_code=404, detail="Design not found")
    
    if new_title is not None:
        design.title = new_title
    if new_description is not None:
        design.description = new_description
    
    db.commit()

    return {"message": "Design updated successfully", "design_id": design_id}

def view_design(db: Session, design_id: int) -> models.Design: 
    design = db.query(models.Design).filter(models.Design.id == design_id).first() 

    if design is None:
        raise HTTPException(status_cide=404, detail="Design not found")
    
    return design

##### DESIGN COMMIT OPERATIONS ####

def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(user_email=comment.user_email, design_id=comment.design_id, content=comment.content)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment: schemas.CommentDelete):
    comment = db.query(models.Comment).filter(models.Comment.id == comment.id).first()

    if not comment :
        # Handle the case where the design does not exist
        raise HTTPException(status_code=404, detail="Design not found")
    
    db.delete(comment)
    db.commit()

def update_comment(db: Session, editComment: schemas.CommentEdit):
    comment = db.query(models.Comment).filter(models.Comment.id == editComment.id).first()
    
    if comment is None:
        # Raise an exception if the design does not exist
        raise HTTPException(status_code=404, detail="Design not found")
    
    comment.content = editComment.content
    
    db.commit()

    return {"message": "Design updated successfully", "comment_id": editComment.id}

def view_comment(db: Session, commentBase: schemas.CommentBase) -> models.Design: 
    comment = db.query(models.Comment).filter(models.Comment.id == commentBase.id).first() 

    if comment is None:
        raise HTTPException(status_cide=404, detail="Design not found")
    
    return comment




