from sqlmodel import select, Session
from app.models.comment import Comment
from sqlalchemy import func


def list_comments(session, post_id: int, limit: int = 10, offset: int = 0) -> tuple[list[Comment], int]:
    statement = select(Comment).where(Comment.post_id == post_id).limit(limit).offset(offset)
    comments = session.exec(statement).all()

    total = session.exec(
        select(func.count()).select_from(Comment).where(Comment.post_id == post_id)
    ).one()

    return comments, total

def create_comment(session: Session, content: str, user_id: int, post_id: int) -> Comment:
    new_comment = Comment(content=content, user_id=user_id, post_id=post_id)
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    
    return new_comment

def get_comment_by_id(session: Session, comment_id: int) -> Comment | None:
    
    return session.get(Comment, comment_id)

def delete_comment(session: Session, comment: Comment) -> None:
    session.delete(comment)
    session.commit()
