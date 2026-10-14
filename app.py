from datetime import date
from typing import Annotated
from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from src.api import auth_router, work_update_router, topic_router
from src.auth import decode_access_token
from src.db import get_db
from src.logger import logger
from src.templates import templates
from src.service_layer import get_recent_work_updates_for_user
from src.utils import greet_user, get_today_logs, sort_logs_by_date, get_user_id_from_cookie


# Main app object
app = FastAPI()

# Add APIRouters
app.include_router(auth_router)
app.include_router(work_update_router)
app.include_router(topic_router)

# Setup templating and static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """
    Middleware to handle authentication
    """
    # Allow white listed routes to pass through
    white_listed_routes = ["/auth/login", "/static"]
    if any(request.url.path.startswith(route) for route in white_listed_routes):
        response = await call_next(request)
        return response
    # Retrieve access token from cookies
    access_token = request.cookies.get("access_token")
    # No access token or Incorrect access token scenario; redirect to login page
    if access_token is None:
        logger.error("No access token provided. Redirecting to login page.")
        return RedirectResponse("/auth/login")
    # Expired access token scenario
    user_details = decode_access_token(access_token)
    if user_details is None:
        logger.error("Invalid or expired access token provided. Redirecting to login page.")
        return RedirectResponse("/auth/login")
    # Valid access token scenario
    initials = f"{user_details.get('first_name', 'U')[0].upper()}{user_details.get('last_name', 'U')[0].upper()}"
    request.state.initials = initials
    response = await call_next(request)
    return response


@app.get("/")
def home_page(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Home page after user is successfully authenticated
    """
    # Retrieve access token from cookies to get user details
    access_token = request.cookies.get("access_token", "")
    user_details = decode_access_token(access_token)
    first_name = user_details.get("first_name", "") if user_details else ""
    user_id = get_user_id_from_cookie(request=request)
    greeting = greet_user(first_name)
    # Get today's date
    today_date = date.today()
    formatted_date = today_date.strftime("%A, %d %B %Y")
    # Get recent daily updates
    recent_work_updates = get_recent_work_updates_for_user(session=db, user_id=user_id)
    recent_work_updates = [update.to_dict() for update in recent_work_updates]
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "greeting": greeting,
            "today_date": formatted_date,
            "name": first_name,
            "recent_work_updates": recent_work_updates
        }
    )
