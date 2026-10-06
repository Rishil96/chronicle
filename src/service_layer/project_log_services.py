"""
This module contains all operations to be performed on the Chronicle Project log functionality
"""
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.db import Projects, ProjectLogs
from src.logger import logger
from src.config import settings, IST


def get_all_projects(session: Session) -> list[Projects]:
    """
    Utility function to get all projects from the Chronicle Projects table
    """
    all_projects = session.execute(select(Projects)).scalars().all()
    return list(all_projects)


def add_project_log(session: Session, log: str, project_id: int, user_id: int) -> None:
    """
    Service layer function to add project logs
    """
    try:
        new_project_log = ProjectLogs(
            log=log,
            project_id=project_id,
            user_id=user_id
        )
        session.add(new_project_log)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to add project log. Error message: {e}")


def get_project_logs(session: Session) -> list[ProjectLogs]:
    """
    This function gets all project logs from the database for past N days
    """
    from_date = datetime.now(tz=IST) - timedelta(days=settings.project_log_days)
    project_logs_list = session.execute(select(ProjectLogs).where(ProjectLogs.created_at >= from_date).order_by(ProjectLogs.created_at.desc())).scalars().all()
    return list(project_logs_list)
