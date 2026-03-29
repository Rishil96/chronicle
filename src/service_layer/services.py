"""
This module contains all operations to be performed on the Chronicle logging app
"""
from datetime import datetime, date, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo
from src.db.models import Logs
from src.db.db_session import DatabaseSession

# Database session
db = DatabaseSession()
IST = ZoneInfo("Asia/Kolkata")


def add_log(session: Session, log_entry: str, use_llm: bool = True) -> None:
    """
    Function to add a log entry to the Chronicle app database
    """
    new_log = Logs(entry=log_entry)
    session.add(new_log)
    session.commit()


def get_logs(session: Session, single_date: date | None = None, from_date: date | None = None, to_date: date | None = None) -> list[Logs]:
    """
    Function to read logs using 2 modes of filtering
        1. Single date
        2. Date range
        Default behavior: returns all logs from last seven days
    """
    # Case 1: Execute for single date
    if single_date is not None:
        stmt = select(Logs).where(Logs.date_of_creation == single_date)
    # Case 2: Execute for time period
    elif from_date is not None and to_date is not None:
        stmt = select(Logs).where(Logs.date_of_creation >= from_date).where(Logs.date_of_creation <= to_date)
    # Case 3: Default behavior
    else:
        to_date = date.today()
        from_date = to_date - timedelta(days=7)
        stmt = select(Logs).where(Logs.date_of_creation >= from_date).where(Logs.date_of_creation <= to_date)

    result = session.execute(stmt).scalars().all()
    return list(result)


def update_log(session: Session, log_id: int, updated_log_entry: str, use_llm: bool = True) -> bool:
    """
    Function to update a log entry using ID
    """
    log_to_update = session.execute(select(Logs).where(Logs.id == log_id)).scalars().one_or_none()
    if log_to_update:
        log_to_update.entry = updated_log_entry
        log_to_update.updated_at = datetime.now(tz=IST)
        session.commit()
        return True
    return False


def delete_log(session: Session, log_id: int):
    """
    Function to delete a log entry using ID
    """
    log_to_delete = session.execute(select(Logs).where(Logs.id == log_id)).scalars().one_or_none()
    if log_to_delete:
        session.delete(log_to_delete)
        session.commit()
        return True
    return False
