from pydantic import BaseModel, constr, validator
from typing import List

class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {
        "from_attributes": True
    }

class CategoryCreateSchema(BaseModel):
    name: constr(min_length=3)
    slug: constr(min_length=3)

    @validator('slug')
    def slug_no_spaces(cls, v):
        if ' ' in v:
            raise ValueError('Slug cannot contain spaces')
        return v

class CategoriesListResponse(BaseModel):
    categories: List[CategoryOut] = []
    limit: int
    offset: int
    total: int

    model_config = {
        "from_attributes": True
    }

class CategoryDeleteMessageOut(BaseModel):
    message: str
