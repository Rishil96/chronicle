from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from src.db import get_db
from src.templates import templates
from src.service_layer import change_password
from src.utils import get_flash, set_flash


# Router object to handle user functionality
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/change-password")
def change_password_page(request: Request):
    """
    Route to render password change form
    """
    flash = get_flash(request=request)
    return templates.TemplateResponse(
        request=request,
        name="change_password.html",
        context={"request": request, "flash": flash},
    )


@router.post("/change-password")
def change_password_form(request: Request, db: Annotated[Session, Depends(get_db)], old_password: str = Form(), new_password: str = Form(), repeat_new_password: str = Form()):
    """
    POST route to handle password changing logic
    """
    # Case 1: Both new password entries are different
    if new_password != repeat_new_password:
        set_flash(request=request, message="New passwords do not match.")
        return RedirectResponse(
            url="/users/change-password",
            status_code=status.HTTP_303_SEE_OTHER
        )
    # Case 2: New password same as old password
    if new_password == old_password:
        set_flash(request=request, message="New password cannot be same as current password.")
        return RedirectResponse(url="/users/change-password", status_code=status.HTTP_303_SEE_OTHER)
    # Call change password service layer
    result = change_password(
        user_id=request.state.user_id,
        current_password=old_password,
        new_password=new_password,
        session=db
    )
    # Case 3: Incorrect current password
    if not result:
        set_flash(request=request, message="Current password is incorrect.")
        return RedirectResponse(
            url="/users/change-password",
            status_code=status.HTTP_303_SEE_OTHER
        )
    # Successful password change scenario
    set_flash(request=request, message="Password changed successfully.", category="success")
    return RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER
    )
