import logging
from datetime import date
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.logger import setup_logger
from src.utils import greet_user

# Load environment variables
load_dotenv()

# Logger Setup
setup_logger()
logger = logging.getLogger("chronicle")


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
