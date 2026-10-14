from datetime import datetime
from typing import List, Dict, Any
from fastapi import HTTPException, Request, status
from src.auth import decode_access_token


# Greeting constants
MORNING = "Good Morning, {user_name}!"
AFTERNOON = "Good Afternoon, {user_name}!"
EVENING = "Good Evening, {user_name}!"
NIGHT = "GO TO SLEEP, {user_name}!"


def greet_user(name):
    """
    Utility function to greet user
    """
    curr_time_hour = datetime.now().time().hour
    if 5 <= curr_time_hour < 12:
        return MORNING.format(user_name=name)
    elif 12 <= curr_time_hour < 16:
        return AFTERNOON.format(user_name=name)
    elif 16 <= curr_time_hour < 21:
        return EVENING.format(user_name=name)
    return NIGHT.format(user_name=name)


def sort_work_updates_by_date(updates_list: List[dict]) -> Dict[Any, Any]:
    """
    Utility Function to sort logs by date
    """
    work_updates_by_date = {}
    for log in updates_list:
        log_date = log["date_of_creation"]
        if log_date not in work_updates_by_date:
            work_updates_by_date[log_date] = []
        work_updates_by_date[log_date].append(log)
    # Sort history dict by date in descending order
    work_updates_by_date = dict(sorted(work_updates_by_date.items(), reverse=True))
    return work_updates_by_date


def get_user_id_from_cookie(request: Request) -> int:
    """
    Utility Function to get user id from cookie
    """
    # Read user ID from cookie
    access_token = request.cookies.get("access_token", "")
    user_details = decode_access_token(access_token)
    user_id = user_details.get("user_id") if user_details else None
    if not isinstance(user_id, int):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not a valid login session by user. Please log in again.")
    return user_id
