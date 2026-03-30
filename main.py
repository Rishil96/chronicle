import logging
from fastapi import FastAPI


logger = logging.getLogger("chronicle")
logger.setLevel(logging.INFO)


app = FastAPI()
@app.get("/")
def home():
    return {
        "message": "Chronicle App!"
    }
