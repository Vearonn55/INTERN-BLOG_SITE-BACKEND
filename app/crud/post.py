from sqlmodel import select, Session
from app.models.post import Post
from typing import List, Tuple
from sqlalchemy import func


def list_posts(session: Session, limit: int = 10, offset: int = 0) -> Tuple[List[Post], int]:
    # Query posts with pagination
    statement = select(Post).where(Post.published == True).limit(limit).offset(offset)
    posts = session.exec(statement).all()

    # Get total count of published posts (ignoring limit/offset)
    total = session.exec(select(func.count()).select_from(Post).where(Post.published == True)).one()

    return posts, total

def get_post_by_id(session: Session, post_id: int) -> Post | None:
    
    return session.get(Post, post_id)

def create_post(session: Session, title: str, slug: str, content: str, image_url: str | None, category_id: int, published: bool, author_id: int) -> Post:
    new_post = Post(
        title=title,
        slug=slug,
        content=content,
        image_url=image_url,
        category_id=category_id,
        published=published,
        author_id=author_id
    )
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    
    return new_post

def update_post(session: Session, post: Post, title: str, slug: str, content: str, image_url: str | None, category_id: int, published: bool) -> Post:
    post.title = title
    post.slug = slug
    post.content = content
    post.image_url = image_url
    post.category_id = category_id
    post.published = published

    session.add(post)
    session.commit()
    session.refresh(post)
    
    return post

def delete_post(session: Session, post: Post) -> None:
    session.delete(post)
    session.commit()

def list_unpublished_posts(session: Session, limit: int = 10, offset: int = 0) -> list[Post]:
    statement = select(Post).where(Post.published == False).limit(limit).offset(offset)

    return session.exec(statement).all()

def count_unpublished_posts(session):

    return session.exec(
        select(func.count()).select_from(Post).where(Post.published == False)
    ).one()

def list_posts_by_author(session: Session, author_id: int, limit: int = 10, offset: int = 0) -> Tuple[List[Post], int]:
    statement = select(Post).where(Post.author_id == author_id).limit(limit).offset(offset)
    posts = session.exec(statement).all()

    total = session.exec(
        select(func.count()).select_from(Post).where(Post.author_id == author_id)
    ).one()

    return posts, total
