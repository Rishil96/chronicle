import os
from typing import List, Dict, Any
from datetime import datetime, date
from sqlalchemy.orm import Session
from src.service_layer import get_logs


# Greeting constants
MORNING = "Good Morning, {user_name}!"
AFTERNOON = "Good Afternoon, {user_name}!"
EVENING = "Good Evening, {user_name}!"
NIGHT = "GO TO SLEEP, {user_name}!"


def greet_user():
    """
    Utility function to greet user
    """
    user_name = os.getenv("USER_NAME")
    curr_time_hour = datetime.now().time().hour
    if 5 <= curr_time_hour < 12:
        return MORNING.format(user_name=user_name)
    elif 12 <= curr_time_hour < 16:
        return AFTERNOON.format(user_name=user_name)
    elif 16 <= curr_time_hour < 21:
        return EVENING.format(user_name=user_name)
    return NIGHT.format(user_name=user_name)


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
