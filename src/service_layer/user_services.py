"""
This module contains all operations to be performed on the Chronicle Users functionality
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth import hash_password, verify_password
from src.db import Users
from src.logger import logger


def change_password(user_id: int, current_password: str, new_password: str, session: Session) -> bool:
    """
    Service layer function to handle password changing logic
    """
    # Retrieve user password hash from DB
    user = session.execute(select(Users).where(Users.id == user_id)).scalars().one_or_none()
    if user is None:
        logger.error(f"User with id {user_id} does not exist")
        return False
    # Verify password
    if not verify_password(current_password, user.password_hash):
        logger.error("Incorrect password provided by user")
        return False
    # Create new password hash and update it in DB
    new_pw_hash = hash_password(new_password)
    user.password_hash = new_pw_hash
    session.commit()
    return True


def get_all_users(session: Session) -> list[Users]:
    """
    This function gets all users from the database
    """
    all_users = session.execute(select(Users)).scalars().all()
    return list(all_users)
