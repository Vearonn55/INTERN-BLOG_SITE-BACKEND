from sqlmodel import select, Session
from app.models.user import User
from passlib.context import CryptContext
from typing import List, Tuple
from sqlalchemy import func

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()

def get_user_by_username(session: Session, username: str) -> User | None:
    return session.exec(select(User).where(User.username == username)).first()

def create_user(session: Session, username: str, email: str, password: str) -> User:
    hashed_password = pwd_context.hash(password)
    user = User(username=username, email=email, password_hash=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def list_all_users(session: Session, limit: int = 10, offset: int = 0) -> Tuple[List[User], int]:
    users = session.exec(select(User).limit(limit).offset(offset)).all()
    total = session.exec(select(func.count()).select_from(User)).one()
    return users, total

def change_user_role(session: Session, user_id: int, new_role: str) -> User | None:
    user = session.get(User, user_id)
    if not user:
        return None
    user.role = new_role
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
