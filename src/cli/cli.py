import typer
import os
from datetime import date, timedelta
from src.db import DatabaseSession
from src.service_layer import add_log, get_logs, update_log, delete_log
from src.utils import get_today_logs, print_logs, sort_logs_by_date

# Typer CLI application
app = typer.Typer()

# Database session
db_session = DatabaseSession()


# Add a new log
@app.command()
def add(log_entry: str):
    """
    CLI command for adding logs
    """
    with db_session.get_session() as session:
        add_log(session=session, log_entry=log_entry)
    print("New Log added")


# List today's log
@app.command()
def today():
    """
    CLI command to list today's logs
    """
    with db_session.get_session() as session:
        today_logs = get_today_logs(session=session)
    if not today_logs:
        print("No logs found")
        return
    today_date = today_logs[0]["date_of_creation"]
    print_logs(log_date=today_date, logs_list=today_logs)


# History of past N days
@app.command()
def history():
    """
    CLI command to list log history
    """
    history_days = int(os.getenv("HISTORY_DAYS", 30))
    to_date = date.today()
    from_date = to_date - timedelta(days=history_days)
    with db_session.get_session() as session:
        history_log_list = get_logs(session=session, from_date=from_date, to_date=to_date)
        history_log_list = [log.to_dict() for log in history_log_list]
    history_logs_by_date = sort_logs_by_date(logs_list=history_log_list)

    for log_date, log_list in history_logs_by_date.items():
        print_logs(log_date=log_date, logs_list=log_list)
        print("\n")


@app.command()
def update(log_id: int, updated_log: str):
    """
    CLI command to update a log entry using ID
    """
    with db_session.get_session() as session:
        res = update_log(session=session, log_id=log_id, updated_log_entry=updated_log)
    if res:
        print("Log updated")
    else:
        print("Log update failed")

@app.command()
def delete(log_id: int):
    """
    CLI command to delete a log entry using ID
    """
    typer.confirm(f"Are you sure you want to delete this log with ID {log_id}?", abort=True)
    with db_session.get_session() as session:
        res = delete_log(session=session, log_id=log_id)
    if res:
        print("Log deleted")
    else:
        print("Log deletion failed")
