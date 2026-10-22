from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.config import IST
from src.db import get_db
from src.logger import logger
from src.service_layer import add_work_update, get_all_topics, get_work_updates
from src.templates import templates
from src.utils import set_flash, sort_work_updates_by_date

# Router object to handle work updates functionality
router = APIRouter(prefix="/work-updates", tags=["work-updates"])


@router.get("/new")
def work_updates_page(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Page to add a new work update
    """
    # Get today's date
    today_date = datetime.now(tz=IST).date()
    # Get all topics
    topics = get_all_topics(db)
    return templates.TemplateResponse(
        request=request,
        name="add_work_update.html",
        context={
            "topics": topics,
            "display_date": today_date.strftime("%A, %d %B %Y"),
            "iso_date": today_date.isoformat(),
        }
    )

@router.post("")
def new_work_update(request: Request, db: Annotated[Session, Depends(get_db)], topic_id: int = Form(), description: str = Form(), render_date: str = Form()):
    """
    Route to add a new work update via HTML form
    """
    # Read user ID from cookie
    user_id = request.state.user_id
    # Date mismatch scenario
    today_date = datetime.now(tz=IST).date()
    if today_date.isoformat() != render_date:
        logger.warning(f"Date mismatch occurred while adding new work update for user with ID {user_id}. Reloading page.")
        # Get today's date in required formats
        display_date = today_date.strftime("%A, %d %B %Y")
        iso_date = today_date.isoformat()
        # Get all topics
        topics = get_all_topics(db)
        return templates.TemplateResponse(
            request=request,
            name="add_work_update.html",
            context={
                "topics": topics,
                "display_date": display_date,
                "iso_date": iso_date,
                "description": description,
                "selected_topic": topic_id,
                "flash": {
                    "message": "Date mismatch. Your update is kept below, so please submit again.",
                    "category": "error"
                }
            }
        )
    # Make database entry
    result, message = add_work_update(session=db, user_id=user_id, topic_id=topic_id, description=description)
    if result:
        logger.info(f"New work update added. User ID: {user_id} | Topic ID: {topic_id}")
        set_flash(
            request=request,
            message=message,
            category="success"
        )
    else:
        logger.error(f"Failed to add new work update. Error: {message}")
        set_flash(
            request=request,
            message=message,
            category="error"
        )
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("")
def all_work_updates(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Page to view work updates of colleagues for the past week
    """
    # Read daily updates for past N days
    past_updates = get_work_updates(db)
    past_updates = [past_update.to_dict() for past_update in past_updates]
    past_updates = sort_work_updates_by_date(past_updates)
    return templates.TemplateResponse(
        request=request,
        name="work_updates.html",
        context={"past_updates": past_updates}
    )
