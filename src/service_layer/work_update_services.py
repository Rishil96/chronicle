"""
This module contains all operations to be performed on the Chronicle Daily updates functionality
"""
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.config import settings, IST
from src.db import WorkUpdates, Topics, Users
from src.logger import logger


def get_all_topics(session: Session) -> list[Topics]:
    """
    This function gets all work update topics from the database
    """
    categories = session.execute(select(Topics)).scalars().all()
    return list(categories)


def add_new_topic(session: Session, topic_name: str, description: str, created_by_id: int) -> None:
    """
    Service layer function to add a new topic
    """
    try:
        new_topic = Topics(
            topic_name=topic_name,
            description=description,
            created_by_id=created_by_id
        )
        session.add(new_topic)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to add a new topic. Error message: {e}")


def add_work_update(session: Session, user_id: int, topic_id: int, description: str) -> None:
    """
    Service function which accepts work update data and makes an entry into the database
    """
    try:
        new_work_update = WorkUpdates(
            topic_id=topic_id,
            description=description,
            user_id=user_id
        )
        session.add(new_work_update)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to add work update. Error message: {e}")


def get_work_updates(session: Session) -> list[WorkUpdates]:
    """
    This function gets all work updates from the database for past N days
    """
    from_date = datetime.now(tz=IST) - timedelta(days=settings.work_update_history_days)
    work_updates_list = session.execute(select(WorkUpdates).where(WorkUpdates.created_at >= from_date).order_by(WorkUpdates.created_at.desc())).scalars().all()
    return list(work_updates_list)


def get_recent_work_updates_for_user(session: Session, user_id: int) -> list[WorkUpdates]:
    """
    Service layer function to get recently made work updates by a user
    """
    from_date = datetime.now(tz=IST) - timedelta(hours=settings.recency_hours)
    recent_updates = session.execute(select(WorkUpdates).where(WorkUpdates.user_id == user_id).where(WorkUpdates.created_at >= from_date)).scalars().all()
    return list(recent_updates)


def get_user_by_email(session: Session, email: str) -> Users | None:
    """
    Service layer function to get a user by email
    """
    try:
        user_fetch_stmt = select(Users).where(Users.email == email)
        user = session.execute(user_fetch_stmt).scalars().one_or_none()
        if user is None:
            logger.error(f"User not found: {email}")
        return user
    except Exception as e:
        logger.error(f"Error while fetching user via email: {e}")
        return None
