from pydantic import BaseModel


class CommentBase(BaseModel):
    id: int

class CommentCreate(BaseModel):
    content: str
    design_id: int
    user_email: str

class CommentResponse(CommentCreate):
    pass

class CommentDelete(CommentBase):
    pass

class CommentEdit(CommentBase):
    content: str

class CommentView(CommentBase):
    content: str
    design_id: int
    user_email: str
    
