from datetime import datetime
from typing import List, Dict, Any
from fastapi import Request


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


def set_flash(request: Request, message: str, category: str = "error") -> None:
    """
    Utility Function to set flash message
    """
    request.session["flash"] = {
        "message": message,
        "category": category
    }


def get_flash(request: Request) -> dict | None:
    """
    Utility Function to get flash message
    """
    return request.session.pop("flash", None)
