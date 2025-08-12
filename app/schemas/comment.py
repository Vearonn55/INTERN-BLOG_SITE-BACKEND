from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional, List

class CommentOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    user_id: int
    post_id: int

    model_config = {
        "from_attributes": True
    }

class CommentCreateSchema(BaseModel):
    content: constr(min_length=1)

    model_config = {
        "from_attributes": True
    }

class CommentsListResponse(BaseModel):
    comments: List[CommentOut] = []
    limit: int
    offset: int
    total: int  # total number of comments for the post

    model_config = {
        "from_attributes": True
    }

class CommentDeleteMessageOut(BaseModel):
    message: str
