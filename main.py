import logging
import os
from datetime import date, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.db import DatabaseSession
from src.logger import setup_logger
from src.service_layer import add_log, get_logs, delete_log, get_log_by_id, update_log
from src.utils import greet_user, get_today_logs

# Load environment variables
load_dotenv()

# Logger Setup
setup_logger()
logger = logging.getLogger("chronicle")

# Database session setup
db = DatabaseSession()

app = FastAPI()
# Setup templating and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    """
    Home page
    """
    greeting = greet_user()
    today_date = date.today()
    formatted_date = today_date.strftime("%A, %d %B %Y")
    with db.get_session() as session:
        today_log_list = get_logs(session=session, single_date=today_date)
        today_log_list = [log.to_dict() for log in today_log_list]
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"greeting": greeting, "today_date": formatted_date, "logs": today_log_list}
    )


@app.get("/history")
def history(request: Request):
    """
    History page
    """
    history_days = int(os.getenv("HISTORY_DAYS", 30))
    to_date = date.today()
    from_date = to_date - timedelta(days=history_days)
    with db.get_session() as session:
        history_log_list = get_logs(session=session, from_date=from_date, to_date=to_date)
        history_log_list = [log.to_dict() for log in history_log_list]
    # Group logs by date
    history_logs_by_date = {}
    for log in history_log_list:
        log_date = log["date_of_creation"]
        if log_date not in history_logs_by_date:
            history_logs_by_date[log_date] = []
        history_logs_by_date[log_date].append(log)

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={"logs_by_date": history_logs_by_date}
    )


@app.get("/filter")
def filter_logs(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="filter.html",
        context={}
    )


@app.post("/logs")
def add_logs(request: Request, log_entry: str = Form(...)):
    """
    Route to add a log entry via HTMX from Home route
    """
    with db.get_session() as session:
        add_log(session=session, log_entry=log_entry)
        today_date = date.today()
        today_log_list = get_logs(session=session, single_date=today_date)
        today_log_list = [log.to_dict() for log in today_log_list]
    return templates.TemplateResponse(
        request=request,
        name="_logs_list.html",
        context={"logs": today_log_list}
    )


@app.delete("/logs/{log_id}")
def delete_logs(request: Request, log_id: int):
    """
    Route to delete a log entry via log ID
    """
    with db.get_session() as session:
        delete_log(session=session, log_id=log_id)
        today_log_list = get_today_logs(session=session)
    return templates.TemplateResponse(
        request=request,
        name="_logs_list.html",
        context={"logs": today_log_list}
    )


@app.get("/logs/{log_id}/edit")
def edit_logs(request: Request, log_id: int):
    """
    Route to edit a log entry via log ID
    """
    with db.get_session() as session:
        log_to_edit = get_log_by_id(session=session, log_id=log_id)
    return templates.TemplateResponse(
        request=request,
        name="_log_edit_form.html",
        context={"log": log_to_edit}
    )


@app.put("/logs/{log_id}")
def update_logs(request: Request, log_id: int, log_entry: str = Form(...)):
    """
    Route to update a log entry via log ID
    """
    with db.get_session() as session:
        update_log(session=session, log_id=log_id, updated_log_entry=log_entry)
        today_log_list = get_today_logs(session=session)
    return templates.TemplateResponse(
        request=request,
        name="_logs_list.html",
        context={"logs": today_log_list}
    )


@app.get("/logs/{log_id}/cancel")
def cancel_log_update(request: Request, log_id: int):
    """
    Route to cancel a log entry via log ID and return partial to recreate original log list item
    """
    with db.get_session() as session:
        log = get_log_by_id(session=session, log_id=log_id)
    return templates.TemplateResponse(
        request=request,
        name="_log_item.html",
        context={"log": log}
    )
