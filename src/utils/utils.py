import random
from typing import Any

from fastapi import Request

# Greeting constants
GREETINGS = [
    "Hello, {name}!",
    "Welcome back, {name}!",
    "Good to see you, {name}.",
    "Hi {name}!",
    "Hey {name}!",
]


def greet_user(name):
    """
    Utility function to greet user
    """
    return random.choice(GREETINGS).format(name=name)


def sort_work_updates_by_date(updates_list: list[dict]) -> dict[Any, Any]:
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
