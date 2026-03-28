"""
This module contains all operations to be performed on the Chronicle logging app
"""
from datetime import date
from sqlalchemy.orm import Session


def add_log(session: Session, log_entry: str, use_llm: bool = True):
    raise NotImplementedError


def get_logs(session: Session, single_date: date | None = None, from_date: date | None = None, to_date: date | None = None):
    raise NotImplementedError


def update_log(session: Session, log_id: int, updated_log_entry: str, use_llm: bool = True):
    raise NotImplementedError


def delete_log(session: Session, log_id: int):
    raise NotImplementedError
