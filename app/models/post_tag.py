from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class PostTag(SQLModel, table=True):
    __tablename__ = "post_tags"

    post_id: int = Field(foreign_key="posts.id", primary_key=True, nullable=False)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True, nullable=False)

    post: Optional["Post"] = Relationship(back_populates="tags")
    tag: Optional["Tag"] = Relationship(back_populates="posts")
