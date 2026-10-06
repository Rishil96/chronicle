from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from src.db import get_db
from src.logger import logger
from src.service_layer import get_all_categories, add_daily_update, get_daily_updates
from src.templates import templates
from src.utils import sort_logs_by_date, get_user_id_from_cookie


# Router object to handle daily updates functionality
router = APIRouter(prefix="/daily-updates", tags=["daily-updates"])


@router.get("/new")
def daily_update_page(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Page to add a new daily update
    """
    categories = get_all_categories(db)
    return templates.TemplateResponse(
        request=request,
        name="add_daily_update.html",
        context={"categories": categories}
    )

@router.post("")
def new_daily_update(request: Request, db: Annotated[Session, Depends(get_db)], category: str = Form(), summary: str = Form(), description: str = Form()):
    """
    Route to add a new daily update via HTML form
    """
    # Read user ID from cookie
    user_id = get_user_id_from_cookie(request=request)
    # Make database entry
    add_daily_update(session=db, user_id=user_id, category=category, summary=summary, description=description)
    logger.info(f"New daily update added. User ID: {user_id} | Category: {category}")
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("")
def all_daily_updates(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Page to view daily updates of colleagues for the past week
    """
    # Read daily updates for past N days
    past_updates = get_daily_updates(db)
    past_updates = [past_update.to_dict() for past_update in past_updates]
    past_updates = sort_logs_by_date(past_updates)
    return templates.TemplateResponse(
        request=request,
        name="daily_updates.html",
        context={"past_updates": past_updates}
    )


@router.put("/{daily_update_id}")
def edit_daily_update(daily_update_id: int):
    """
    Route to edit a daily update
    """
    pass


@router.delete("/{daily_update_id}")
def delete_daily_update(daily_update_id: int):
    """
    Route to delete a daily update
    """
    pass
