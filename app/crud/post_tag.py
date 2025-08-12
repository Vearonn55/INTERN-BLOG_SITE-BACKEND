from sqlmodel import select
from app.models.post_tag import PostTag
from app.engine import get_session

def get_post_tags_by_post_id(post_id: int) -> list[PostTag]:
    with next(get_session()) as session:
        
        return session.exec(select(PostTag).where(PostTag.post_id == post_id)).all()
