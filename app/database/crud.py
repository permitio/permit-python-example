import base64
from typing import Any, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.comments.schemas import CommentBase, CommentCreate, CommentDelete, CommentEdit
from app.routers.designs.schemas import DesignCreate, DesignDelete

from app.database.models import User, Design, Comment

##### USER CRUD OPERATIONS ####




async def get_user(db_session: AsyncSession, user: Any) -> User:
     # Construct a query to find a user by email
    # statement = select(User).where(User.email == user.email)
    db_user = (await db_session.scalars(select(User).where(User.email == user.email))).first()

    # Execute the query
    # result = await db.execute(select(User))
    
    # Fetch the first result
    # db_user = result.scalars().first()
    
    return db_user 

async def create_user(db: AsyncSession, user: Any):
    fake_hashed_password = base64.b64encode(user.password.encode()).decode()  # Ensure password is encoded and decoded correctly
    db_user = User(email=user.email, hash_pwd=fake_hashed_password, name=user.name)
    await db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

##### DESIGN CRUD OPERATIONS ####

async def create_design(db: AsyncSession, design: DesignCreate) -> Design:
    db_design = Design(user_email=design.user_email, title=design.title, description=design.description)
    db.add(db_design)
    await db.commit()
    await db.refresh(db_design)

    return db_design

async def delete_design(db: AsyncSession, deleteDesign: DesignDelete) -> int:
    result = await db.execute(select(Design).filter(Design.id == deleteDesign.id))
    design = result.scalars().first()

    if not design:
        # Handle the case where the design does not exist
        raise HTTPException(status_code=404, detail="Design not found")
    
    await db.delete(design)
    await db.commit()

    return design.id

async def edit_design(db: AsyncSession, design_id: int, new_title: Optional[str] = None, new_description: Optional[str] = None):
    result = await db.execute(select(Design).filter(Design.id == design_id))
    design = result.scalars().first()
    
    if design is None:
        # Raise an exception if the design does not exist
        raise HTTPException(status_code=404, detail="Design not found")
    
    if new_title is not None:
        design.title = new_title
    if new_description is not None:
        design.description = new_description
    
    await db.commit()

    return design_id

async def view_design(db: AsyncSession, design_id: int) -> Design: 
    result = await db.execute(select(Design).filter(Design.id == design_id))
    design = result.scalars().first()

    if design is None:
        raise HTTPException(status_code=404, detail="Design not found")
    
    return design

##### COMMENT CRUD OPERATIONS ####

async def create_comment(db: AsyncSession, comment: CommentCreate):
    db_comment = Comment(user_email=comment.user_email, design_id=comment.design_id, content=comment.content)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def delete_comment(db: AsyncSession, comment: CommentDelete):
    result = await db.execute(select(Comment).filter(Comment.id == comment.id))
    comment = result.scalars().first()

    if not comment:
        # Handle the case where the comment does not exist
        raise HTTPException(status_code=404, detail="Comment not found")
    
    await db.delete(comment)
    await db.commit()

async def update_comment(db: AsyncSession, editComment: CommentEdit):
    result = await db.execute(select(Comment).filter(Comment.id == editComment.id))
    comment = result.scalars().first()
    
    if comment is None:
        # Raise an exception if the comment does not exist
        raise HTTPException(status_code=404, detail="Comment not found")
    
    comment.content = editComment.content
    
    await db.commit()

    return editComment.id

async def view_comment(db: AsyncSession, commentBase: CommentBase) -> Comment: 
    result = await db.execute(select(Comment).filter(Comment.id == commentBase.id))
    comment = result.scalars().first()

    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    return comment
