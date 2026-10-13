from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from src.db import get_db
from src.logger import logger
from src.service_layer import get_all_topics, add_work_update, get_work_updates
from src.templates import templates
from src.utils import sort_logs_by_date, get_user_id_from_cookie


# Router object to handle work updates functionality
router = APIRouter(prefix="/work-updates", tags=["work-updates"])


@router.get("/new")
def work_updates_page(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Page to add a new daily update
    """
    topics = get_all_topics(db)
    return templates.TemplateResponse(
        request=request,
        name="add_work_update.html",
        context={"topics": topics}
    )

@router.post("")
def new_work_update(request: Request, db: Annotated[Session, Depends(get_db)], topic_id: int = Form(), description: str = Form()):
    """
    Route to add a new work update via HTML form
    """
    # Read user ID from cookie
    user_id = get_user_id_from_cookie(request=request)
    # Make database entry
    add_work_update(session=db, user_id=user_id, topic_id=topic_id, description=description)
    logger.info(f"New daily update added. User ID: {user_id} | Topic ID: {topic_id}")
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("")
def all_work_updates(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Page to view work updates of colleagues for the past week
    """
    # Read daily updates for past N days
    past_updates = get_work_updates(db)
    past_updates = [past_update.to_dict() for past_update in past_updates]
    past_updates = sort_logs_by_date(past_updates)
    return templates.TemplateResponse(
        request=request,
        name="work_updates.html",
        context={"past_updates": past_updates}
    )
