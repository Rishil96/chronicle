from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from src.auth import create_access_token, verify_password
from src.db import get_db, Users
from src.logger import logger
from src.service_layer import get_user_by_email
from src.templates import templates


# Router object to handle authentication functionality
router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
def login_page(request: Request):
    """
    GET login route to render login page
    """
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@router.post("/login")
def login_user(email: str = Form(), password: str = Form(), session: Session = Depends(get_db)):
    """
    POST login route to log in user
    """
    # Retrieve user by email
    # Case 1: User not found
    user: Users | None = get_user_by_email(session, email)
    if user is None:
        logger.error(f"User with email {email} not found")
        return RedirectResponse(
            url="/auth/login",
            status_code=status.HTTP_303_SEE_OTHER
        )
    # Case 2: Incorrect credentials
    if not verify_password(password, user.password_hash):
        logger.error(f"Incorrect password entered for email {email}")
        return RedirectResponse(
            url="/auth/login",
            status_code=status.HTTP_303_SEE_OTHER
        )
    # Case 3: Successful user authentication
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id, "first_name": user.first_name},
    )
    response = RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax")
    return response


@router.get("/logout")
def logout():
    """
    Route to log out user from the session
    """
    response = RedirectResponse(
        url="/auth/login",
        status_code=status.HTTP_303_SEE_OTHER
    )
    response.delete_cookie(key="access_token")
    return response
