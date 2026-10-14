from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from src.db import get_db
from src.templates import templates
from src.service_layer import change_password


# Router object to handle user functionality
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/change-password")
def change_password_page(request: Request):
    """
    Route to render password change form
    """
    return templates.TemplateResponse(
        request=request,
        name="change_password.html",
        context={"request": request},
    )


@router.post("/change-password")
def change_password_form(request: Request, db: Annotated[Session, Depends(get_db)], old_password: str = Form(), new_password: str = Form(), repeat_new_password: str = Form()):
    """
    POST route to handle password changing logic
    """
    # Compare new password with it's repeated version
    if new_password != repeat_new_password:
        return RedirectResponse(
            url="/users/change-password",
            status_code=status.HTTP_303_SEE_OTHER
        )
    # Call change password service layer
    result = change_password(
        user_id=request.state.user_id,
        current_password=old_password,
        new_password=new_password,
        session=db
    )
    # Failed to change password scenario
    if not result:
        return RedirectResponse(
            url="/users/change-password",
            status_code=status.HTTP_303_SEE_OTHER
        )
    # Successful password change scenario
    return RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER
    )
