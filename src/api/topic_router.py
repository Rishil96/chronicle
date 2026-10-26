from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.db import get_db
from src.logger import logger
from src.service_layer import add_new_topic
from src.templates import templates
from src.utils import set_flash

# Router object to handle topics functionality
router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("/new")
def add_topic_page(request: Request):
    """
    Page to add a new topic for work updates
    """
    return templates.TemplateResponse(
        request=request,
        name="add_new_topic.html",
        context={"request": request}
    )


@router.post("")
def new_topic(request: Request, db: Annotated[Session, Depends(get_db)], topic_name: str = Form(), description: str = Form()):
    """
    POST route to add a new topic
    """
    # Read user ID from request state
    user_id = request.state.user_id
    # Add new topic
    result, message = add_new_topic(session=db, topic_name=topic_name, description=description, created_by_id=user_id)
    if result:
        logger.info(f"New Topic added | User ID: {user_id} | Topic Name: {topic_name}")
        set_flash(
            request=request,
            message=message,
            category="success"
        )
    else:
        logger.error(f"Failed to add new topic. Error: {message}")
        set_flash(
            request=request,
            message=message,
            category="error"
        )
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
