import logging
from fastapi import FastAPI
from src.logger import setup_logger


setup_logger()
logger = logging.getLogger("chronicle")


app = FastAPI()
@app.get("/")
def home():
    return {
        "message": "Chronicle App!"
    }
