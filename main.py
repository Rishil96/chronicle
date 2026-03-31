import logging
from datetime import date
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.db import DatabaseSession
from src.logger import setup_logger
from src.service_layer import add_log, get_logs
from src.utils import greet_user

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
    greeting = greet_user()
    today_date = date.today().strftime("%A, %d %B %Y")
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"request": request, "greeting": greeting, "today_date": today_date}
    )


@app.get("/history")
def history(request: Request):
    return templates.TemplateResponse(request,"history.html", {"request": request})


@app.get("/filter")
def filter_logs(request: Request):
    return templates.TemplateResponse(request,"filter.html", {"request": request})


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
        print(today_log_list)
    return templates.TemplateResponse(
        request=request,
        name="_logs_list.html",
        context={"logs": today_log_list}
    )
