from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from src.auth import decode_access_token
from src.db import get_db
from src.logger import logger
from src.service_layer import get_all_categories, add_daily_update
from src.templates import templates


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
def new_daily_update(request: Request, category: str = Form(), summary: str = Form(), description: str = Form(), session: Session = Depends(get_db)):
    """
    Route to add a new daily update via HTML form
    """
    # Read user ID from cookie
    access_token = request.cookies.get("access_token", "")
    user_details = decode_access_token(access_token)
    user_id = user_details.get("user_id")
    if not isinstance(user_id, int):
        raise HTTPException(status_code=404, detail="Not a valid login session by user. Please log in again.")
    # Make database entry
    add_daily_update(session=session, user_id=user_id, category=category, summary=summary, description=description)
    logger.info(f"New daily update added. User ID: {user_id} | Category: {category}")
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("")
def all_daily_updates():
    """
    Page to view daily updates of colleagues for the past week
    """
    pass


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
