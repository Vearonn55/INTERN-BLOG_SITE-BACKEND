from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    slug: str = Field(nullable=False, unique=True)

    posts: List["PostTag"] = Relationship(back_populates="tag")
