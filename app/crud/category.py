from sqlmodel import select, Session
from app.models.category import Category
from sqlalchemy import func

def list_categories(session, limit: int = 10, offset: int = 0) -> tuple[list[Category], int]:
    categories = session.exec(
        select(Category).limit(limit).offset(offset)
    ).all()

    total = session.exec(
        select(func.count()).select_from(Category)
    ).one()

    return categories, total


def get_category_by_id(session: Session, cat_id: int) -> Category | None:
    
    return session.get(Category, cat_id)

def get_category_by_name_or_slug(session: Session, name: str, slug: str) -> Category | None:
    
    return session.exec(
        select(Category).where(
            (Category.name == name) | (Category.slug == slug)
        )
    ).first()

def create_category(session: Session, name: str, slug: str) -> Category:
    new_cat = Category(name=name, slug=slug)
    session.add(new_cat)
    session.commit()
    session.refresh(new_cat)
    
    return new_cat

def delete_category(session: Session, cat: Category) -> None:
    session.delete(cat)
    session.commit()
