from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    slug: str = Field(nullable=False, unique=True)
    content: str = Field(nullable=False)
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = None
    published: bool = Field(default=False, nullable=False)

    author_id: int = Field(foreign_key="users.id", nullable=False)
    author: Optional["User"] = Relationship(back_populates="posts")

    category_id: int = Field(foreign_key="categories.id", nullable=False)
    category: Optional["Category"] = Relationship(back_populates="posts")

    tags: List["PostTag"] = Relationship(back_populates="post", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    comments: List["Comment"] = Relationship(back_populates="post")
