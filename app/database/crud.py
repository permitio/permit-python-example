import base64
from typing import Any, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.routers.comments.schemas import CommentBase, Comment, CommentDelete, CommentEdit
from app.routers.designs.schemas import DesignCreate, DesignDelete
from app.database.models import User, Design, Comment

##### USER CRUD OPERATIONS ####

async def get_user(db_session: AsyncSession, user: Any) -> User:
    db_user = (await db_session.scalars(select(User).where(User.email == user.email))).first()

    return db_user 

async def create_user(db_session: AsyncSession, user: Any) -> User:
    fake_hashed_password = base64.b64encode(user.password.encode()).decode()  # Ensure password is encoded and decoded correctly
    db_user = User(email=user.email, hash_pwd=fake_hashed_password, name=user.name)
    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)
    return db_user

##### DESIGN CRUD OPERATIONS ####

async def get_design(db_session: AsyncSession, design: Design) -> User:
    design = (await db_session.scalars(select(Design).where(Design.id == design.id))).first()

    return design 

async def create_design(db_session: AsyncSession, design: DesignCreate) -> Design:
    db_design = Design(user_email=design.user_email, title=design.title, description=design.description)
    db_session.add(db_design)
    await db_session.commit()
    await db_session.refresh(db_design)

    return db_design

async def delete_design(db_session: AsyncSession, deleteDesign: DesignDelete) -> int:
    result = await db_session.execute(select(Design).filter(Design.id == deleteDesign.id))
    design = result.scalars().first()

    if not design:
        # Handle the case where the design does not exist
        raise HTTPException(status_code=404, detail="Design not found")
    
    await db_session.delete(design)
    await db_session.commit()

    return design.id

async def edit_design(db_session: AsyncSession, design_id: int, new_title: Optional[str] = None, new_description: Optional[str] = None):
    result = await db_session.execute(select(Design).filter(Design.id == design_id))
    design = result.scalars().first()
    
    if design is None:
        # Raise an exception if the design does not exist
        raise HTTPException(status_code=404, detail="Design not found")
    
    if new_title is not None:
        design.title = new_title
    if new_description is not None:
        design.description = new_description
    
    await db_session.commit()

    return design_id

async def view_design(db_session: AsyncSession, design_id: int) -> Design: 
    result = await db_session.execute(select(Design).filter(Design.id == design_id))
    design = result.scalars().first()

    if design is None:
        raise HTTPException(status_code=404, detail="Design not found")
    
    return design

##### COMMENT CRUD OPERATIONS ####

async def create_comment(db_session: AsyncSession, comment: Comment):
    db_comment = Comment(user_email=comment.user_email, design_id=comment.design_id, content=comment.content)
    db_session.add(db_comment)
    await db_session.commit()
    await db_session.refresh(db_comment)
    return db_comment

async def delete_comment(db_session: AsyncSession, comment: CommentDelete) -> Comment :
    result = await db_session.execute(select(Comment).filter(Comment.id == comment.id))
    comment = result.scalars().first()

    if not comment:
        # Handle the case where the comment does not exist
        raise HTTPException(status_code=404, detail="Comment not found")
    
    await db_session.delete(comment)
    await db_session.commit()

    return comment

async def update_comment(db_session: AsyncSession, editComment: CommentEdit):
    result = await db_session.execute(select(Comment).filter(Comment.id == editComment.id))
    comment = result.scalars().first()
    
    if comment is None:
        # Raise an exception if the comment does not exist
        raise HTTPException(status_code=404, detail="Comment not found")
    
    comment.content = editComment.content
    
    await db_session.commit()

    return editComment.id

async def view_comment(db_session: AsyncSession, commentBase: CommentBase) -> Comment: 
    result = await db_session.execute(select(Comment).filter(Comment.id == commentBase.id))
    comment = result.scalars().first()

    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    return comment
