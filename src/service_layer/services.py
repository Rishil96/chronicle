"""
This module contains all operations to be performed on the Chronicle logging app
"""
from datetime import datetime, date
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.db.models import Logs
from src.db.db_session import DatabaseSession

# Database session
db = DatabaseSession()


def add_log(session: Session, log_entry: str, use_llm: bool = True):
    """
    Function to add a log entry to the Chronicle app database
    """
    new_log = Logs(entry=log_entry)
    session.add(new_log)
    session.commit()

def get_logs(session: Session, single_date: date | None = None, from_date: date | None = None, to_date: date | None = None):
    raise NotImplementedError


def update_log(session: Session, log_id: int, updated_log_entry: str, use_llm: bool = True):
    raise NotImplementedError


def delete_log(session: Session, log_id: int):
    raise NotImplementedError
