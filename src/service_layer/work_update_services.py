"""
This module contains all operations to be performed on the Chronicle Daily updates functionality
"""
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.config import settings, IST
from src.db import WorkUpdates, Topics
from src.logger import logger


def get_all_topics(session: Session) -> list[Topics]:
    """
    This function gets all work update topics from the database
    """
    categories = session.execute(select(Topics)).scalars().all()
    return list(categories)


def add_work_update(session: Session, user_id: int, topic_id: int, description: str) -> None:
    """
    Utility function which accepts work update data and makes an entry into the database
    """
    try:
        new_daily_update = WorkUpdates(
            topic_id=topic_id,
            description=description,
            user_id=user_id
        )
        session.add(new_daily_update)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to add work update. Error message: {e}")


def get_daily_updates(session: Session) -> list[WorkUpdates]:
    """
    This function gets all daily updates from the database for past N days
    """
    from_date = datetime.now(tz=IST) - timedelta(days=settings.daily_updates_days)
    daily_updates_list = session.execute(select(WorkUpdates).where(WorkUpdates.created_at >= from_date).order_by(WorkUpdates.created_at.desc())).scalars().all()
    return list(daily_updates_list)


def get_recent_daily_updates_for_user(session: Session, user_id: int) -> list[WorkUpdates]:
    """
    Service layer function to get recently made daily updates by a user
    """
    from_date = datetime.now(tz=IST) - timedelta(hours=settings.recency_hours)
    recent_updates = session.execute(select(WorkUpdates).where(WorkUpdates.user_id == user_id).where(WorkUpdates.created_at >= from_date)).scalars().all()
    return list(recent_updates)
