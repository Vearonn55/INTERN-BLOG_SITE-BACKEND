from pydantic import BaseModel, constr, validator
from typing import Optional, List
from datetime import datetime

class AuthorOut(BaseModel):
    id: int
    username: str

    model_config = {
        "from_attributes": True
    }

class CategoryOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class PostOut(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    image_url: Optional[str]
    created_at: datetime
    published: bool
    author: AuthorOut
    category: CategoryOut

    model_config = {
        "from_attributes": True
    }

class PostsListResponse(BaseModel):
    posts: List[PostOut] = []
    total: int
    limit: int
    offset: int

    model_config = {
        "from_attributes": True
    }

class PostCreateSchema(BaseModel):
    title: constr(min_length=3)
    slug: constr(min_length=3)
    content: str
    image_url: Optional[str] = None
    category_id: int
    published: Optional[bool] = False

    @validator('slug')
    def slug_no_spaces(cls, v):
        if ' ' in v:
            raise ValueError('Slug cannot contain spaces')
        return v

class PostDeleteMessageOut(BaseModel):
    message: str
