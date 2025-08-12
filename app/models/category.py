from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    slug: str = Field(nullable=False, unique=True)

    posts: List["Post"] = Relationship(back_populates="category")
