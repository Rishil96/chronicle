import typer
from src.db import DatabaseSession
from src.service_layer import add_log
from src.utils import get_today_logs

# Typer CLI application
app = typer.Typer()

# Database session
db_session = DatabaseSession()


# Add a new log
@app.command()
def add(log_entry: str):
    with db_session.get_session() as session:
    add_log(session=session, log_entry=log_entry)
    print("New Log added")


# List today's log
@app.command()
def today():
    with db_session.get_session() as session:
        today_logs = get_today_logs(session=session)

    if not today_logs:
        print("No logs found")
        return

    print(f"Date: {today_logs[0]['date_of_creation']}")
    for log in today_logs:
        print(f"{log['id']} | {log['time_of_creation']} | {log['entry']}")

