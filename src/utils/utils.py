from datetime import datetime, date
from typing import List, Dict, Any
from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.auth import decode_access_token
from src.service_layer import get_logs


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


def get_today_logs(session: Session) -> List[dict]:
    today_date = date.today()
    today_log_list = get_logs(session=session, single_date=today_date)
    today_log_list = [log.to_dict() for log in today_log_list]
    return today_log_list


def sort_logs_by_date(logs_list: List[dict]) -> Dict[Any, Any]:
    """
    Utility Function to sort logs by date
    """
    logs_by_date = {}
    for log in logs_list:
        log_date = log["date_of_creation"]
        if log_date not in logs_by_date:
            logs_by_date[log_date] = []
        logs_by_date[log_date].append(log)
    # Sort history dict by date in descending order
    logs_by_date = dict(sorted(logs_by_date.items(), reverse=True))
    return logs_by_date


def print_logs(log_date: date, logs_list: List[dict]):
    """
    Pretty prints logs for a single date
    """
    print(f"\nDate: {log_date}")
    for log in logs_list:
        print(f"{log.get('id')} | {log.get('time_of_creation')} | {log.get('entry')}")


def print_logs_by_date(logs_by_date: dict):
    """
    Pretty prints logs for multiple dates
    """
    for log_date, log_list in logs_by_date.items():
        print_logs(log_date=log_date, logs_list=log_list)


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
