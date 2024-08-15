from pydantic import BaseModel


class CommentBase(BaseModel):
    id: int

class Comment(BaseModel):
    content: str
    design_id: int
    user_email: str

class CommentDelete(CommentBase):
    pass

class CommentEdit(CommentBase):
    content: str

class CommentView(CommentBase):
    content: str
    design_id: int
    user_email: str
    
