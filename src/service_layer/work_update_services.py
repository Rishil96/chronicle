"""
This module contains all operations to be performed on the Chronicle Daily updates functionality
"""
from datetime import date, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.config import IST, settings
from src.db import Topics, Users, WorkUpdates
from src.logger import logger


def get_all_topics(session: Session) -> list[Topics]:
    """
    This function gets all work update topics from the database
    """
    categories = session.execute(select(Topics)).scalars().all()
    return list(categories)


def add_new_topic(session: Session, topic_name: str, description: str, created_by_id: int) -> tuple[bool, str]:
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
        return True, "Successfully added new topic"
    except IntegrityError as e:
        session.rollback()
        logger.error(f"Topic already exists. Error: {e}")
        return False, "Topic already exists"
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Failed to add a new topic. Error message: {e}")
        return False, "Failed to add new topic"

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
    except SQLAlchemyError as e:
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
    recent_updates = session.execute(select(WorkUpdates).where(WorkUpdates.user_id == user_id).where(WorkUpdates.created_at >= from_date).order_by(WorkUpdates.created_at.desc())).scalars().all()
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
    except SQLAlchemyError as e:
        logger.error(f"Error while fetching user via email: {e}")
        return None


def get_filtered_work_updates(session: Session,
                              user_id: int | None,
                              topic_id: int | None,
                              single_date: date | None,
                              from_date: date | None,
                              to_date: date | None) -> list[WorkUpdates]:
    """
    Service layer function to get all work updates from the database based on user applied filters
    """
    # Step 1: Retrieve all work updates
    stmt = select(WorkUpdates)
    # Step 2: Apply user filter
    if user_id:
        stmt = stmt.where(WorkUpdates.user_id == user_id)
    # Step 3: Apply topic filter
    if topic_id:
        stmt = stmt.where(WorkUpdates.topic_id == topic_id)
    # Step 4: Date filter
    if single_date:
        stmt = stmt.where(func.date(WorkUpdates.created_at) == single_date)
    # Step 5: Date Range filter
    elif from_date and to_date:
        stmt = stmt.where(func.date(WorkUpdates.created_at) >= from_date).where(func.date(WorkUpdates.created_at) <= to_date)
    # Step 6: Execute query and return list of work updates
    filtered_work_updates_list = session.execute(stmt.order_by(WorkUpdates.created_at.desc())).scalars().all()
    return list(filtered_work_updates_list)
