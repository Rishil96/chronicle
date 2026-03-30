import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.logger import setup_logger


# Logger Setup
setup_logger()
logger = logging.getLogger("chronicle")


app = FastAPI()
# Setup templating and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request,"home.html", {"request": request})


@app.get("/history")
def history(request: Request):
    return templates.TemplateResponse(request,"history.html", {"request": request})


@app.get("/filter")
def filter_logs(request: Request):
    return templates.TemplateResponse(request,"filter.html", {"request": request})
