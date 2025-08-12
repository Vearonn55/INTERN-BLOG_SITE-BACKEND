from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, unique=True)
    email: str = Field(nullable=False, unique=True)
    password_hash: str = Field(nullable=False)
    role: str = Field(default="admin", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    posts: List["Post"] = Relationship(back_populates="author")
    comments: List["Comment"] = Relationship(back_populates="user")
