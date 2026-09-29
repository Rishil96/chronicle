import logging
import os
from datetime import date, timedelta
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from src.templates import templates
from src.api.auth_router import router as auth_router
from src.auth.auth import decode_access_token
from src.db import DatabaseSession
from src.logger import setup_logger
from src.service_layer import add_log, get_logs, delete_log, get_log_by_id, update_log
from src.utils import greet_user, get_today_logs, sort_logs_by_date


# Logger Setup
setup_logger()
logger = logging.getLogger("chronicle")

# Database session setup
db = DatabaseSession()

app = FastAPI()

# Add APIRouters
app.include_router(auth_router)

# Setup templating and static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """
    Middleware to handle authentication
    """
    # Allow white listed routes to pass through
    white_listed_routes = ["/auth/login", "/static"]
    if any(request.url.path.startswith(route) for route in white_listed_routes):
        response = await call_next(request)
        return response
    # Retrieve access token from cookies
    access_token = request.cookies.get("access_token")
    # No access token or Incorrect access token scenario; redirect to login page
    if access_token is None or decode_access_token(access_token) is None:
        logger.error("No access token provided. Back to the lobby (login route).")
        return RedirectResponse("/auth/login")
    # Valid access token scenario
    response = await call_next(request)
    return response


@app.get("/")
def home_page(request: Request):
    """
    Home page
    """
    greeting = greet_user()
    today_date = date.today()
    formatted_date = today_date.strftime("%A, %d %B %Y")
    with db.get_session() as session:
        today_log_list = get_today_logs(session=session)
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"greeting": greeting, "today_date": formatted_date, "logs": today_log_list}
    )


@app.get("/history")
def history_page(request: Request):
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
    history_logs_by_date = sort_logs_by_date(logs_list=history_log_list)
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={"logs_by_date": history_logs_by_date}
    )


@app.get("/filter")
def filter_page(request: Request):
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
        today_log_list = get_today_logs(session=session)
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


@app.post("/filter")
def filter_logs(request: Request, single_date: date | None = Form(None), from_date: date | None = Form(None), to_date: date | None = Form(None)):
    """
    Route to filter logs via date range and return partial HTML
    """
    with db.get_session() as session:
        if single_date:
            logs = get_logs(session=session, single_date=single_date)
        else:
            logs = get_logs(session=session, from_date=from_date, to_date=to_date)
        logs = [log.to_dict() for log in logs]

    # Group logs by date
    filtered_logs_by_date = sort_logs_by_date(logs_list=logs)

    return templates.TemplateResponse(
        request=request,
        name="_filter_results.html",
        context={"logs_by_date": filtered_logs_by_date}
    )
