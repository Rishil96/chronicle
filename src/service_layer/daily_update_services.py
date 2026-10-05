"""
This module contains all operations to be performed on the Chronicle Daily updates functionality
"""
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.config import settings, IST
from src.db import WorkCategories, DailyUpdates
from src.logger import logger


def get_all_categories(session: Session) -> list[WorkCategories]:
    """
    This function gets all categories from the database
    """
    categories = session.execute(select(WorkCategories)).scalars().all()
    return list(categories)

def add_daily_update(session: Session, user_id: int, category: str, summary: str, description: str) -> None:
    """
    Utility function which accepts daily update data and makes an entry into the database
    """
    try:
        new_daily_update = DailyUpdates(
            category=category,
            summary=summary,
            description=description,
            user_id=user_id
        )
        session.add(new_daily_update)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to add daily update. Error message: {e}")

def get_daily_updates(session: Session) -> list[DailyUpdates]:
    """
    This function gets all daily updates from the database for past N days
    """
    from_date = datetime.now(tz=IST) - timedelta(days=settings.daily_updates_days)
    daily_updates_list = session.execute(select(DailyUpdates).where(DailyUpdates.created_at >= from_date).order_by(DailyUpdates.created_at.desc())).scalars().all()
    return list(daily_updates_list)
