import typer
import os
from datetime import date, timedelta, datetime
from src.db import DatabaseSession
from src.service_layer import add_log, get_logs, update_log, delete_log
from src.utils import get_today_logs, print_logs, sort_logs_by_date, print_logs_by_date

# Typer CLI application
app = typer.Typer()

# Database session
db_session = DatabaseSession()


# Add a new log
@app.command()
def add(log_entry: str):
    """
    Add a new log entry to Chronicle
    """
    with db_session.get_session() as session:
        add_log(session=session, log_entry=log_entry)
    print("New Log added")


# List today's log
@app.command()
def today():
    """
    List all log entries for today
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
    List log entries from the past N days
    """
    history_days = int(os.getenv("HISTORY_DAYS", 30))
    to_date = date.today()
    from_date = to_date - timedelta(days=history_days)
    with db_session.get_session() as session:
        history_log_list = get_logs(session=session, from_date=from_date, to_date=to_date)
        history_log_list = [log.to_dict() for log in history_log_list]
    history_logs_by_date = sort_logs_by_date(logs_list=history_log_list)
    print_logs_by_date(logs_by_date=history_logs_by_date)


@app.command()
def update(log_id: int, updated_log: str):
    """
    Update an existing log entry by ID
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
    Delete a log entry by ID
    """
    typer.confirm(f"Are you sure you want to delete this log with ID {log_id}?", abort=True)
    with db_session.get_session() as session:
        res = delete_log(session=session, log_id=log_id)
    if res:
        print("Log deleted")
    else:
        print("Log deletion failed")


@app.command(name="filter")
def filter_logs(single_date: str | None = typer.Option(None, "--date"),
           from_date: str | None = typer.Option(None, "--from-date"),
           to_date: str | None = typer.Option(None, "--to-date")):
    """
    Filter log entries by a specific date or date range
    """
    # Case 1: Single date present
    if single_date:
        parsed_single_date = datetime.strptime(single_date, "%Y-%m-%d").date()
        with db_session.get_session() as session:
            logs_list = get_logs(session=session, single_date=parsed_single_date)
            logs_list = [log.to_dict() for log in logs_list]
        print_logs(log_date=parsed_single_date, logs_list=logs_list)
        return
    # Case 2: Date range
    if from_date and to_date:
        parsed_from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        parsed_to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
        with db_session.get_session() as session:
            logs_list = get_logs(session=session, from_date=parsed_from_date, to_date=parsed_to_date)
            logs_list = [log.to_dict() for log in logs_list]
        logs_by_date = sort_logs_by_date(logs_list=logs_list)
        print_logs_by_date(logs_by_date=logs_by_date)
        return
    # Case 3: Missing flags
    typer.echo("Please provide either --date or both --from-date and --to-date")
    raise typer.Exit(code=1)
