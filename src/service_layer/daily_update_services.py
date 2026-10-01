"""
This module contains all operations to be performed on the Chronicle Daily updates functionality
"""
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.db.models import WorkCategories


def get_all_categories(session: Session) -> list[WorkCategories]:
    """
    This function gets all categories from the database
    """
    categories = session.execute(select(WorkCategories)).scalars().all()
    return list(categories)
