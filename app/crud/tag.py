from sqlmodel import select
from app.models.tag import Tag
from app.engine import get_session

def get_tag_by_id(tag_id: int) -> Tag | None:
    with next(get_session()) as session:
        
        return session.get(Tag, tag_id)
