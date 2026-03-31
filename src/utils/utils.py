import os
from datetime import datetime


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
