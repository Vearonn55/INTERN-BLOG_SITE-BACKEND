from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user_id: int = Field(foreign_key="users.id", nullable=False)
    user: Optional["User"] = Relationship(back_populates="comments")

    post_id: int = Field(foreign_key="posts.id", nullable=False)
    post: Optional["Post"] = Relationship(back_populates="comments")
