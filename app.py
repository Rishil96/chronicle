from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from src.api import (
    auth_router,
    filter_router,
    topic_router,
    user_router,
    work_update_router,
)
from src.auth import decode_access_token
from src.config import IST, settings
from src.db import get_db
from src.logger import logger
from src.service_layer import get_recent_work_updates_for_user
from src.templates import templates
from src.utils import get_flash, greet_user, set_flash

# Main app object
app = FastAPI()

# Add APIRouters
app.include_router(auth_router)
app.include_router(filter_router)
app.include_router(topic_router)
app.include_router(user_router)
app.include_router(work_update_router)

# Setup templating and static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Helper function to redirect HTMX requests
def redirect_to_login(is_htmx: bool) -> Response | RedirectResponse:
    """
    Helper function to redirect to login page in case of HTMX request failure
    """
    if is_htmx:
        response = Response(status_code=status.HTTP_200_OK)
        response.headers["HX-Redirect"] = "/auth/login"
        return response
    return RedirectResponse("/auth/login", status_code=status.HTTP_303_SEE_OTHER)


# Add app middlewares
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
    # Check if request is via HTMX
    is_htmx = bool(request.headers.get("HX-Request"))
    # Missing access token scenario
    if access_token is None:
        logger.error("No access token provided. Redirecting to login page.")
        return redirect_to_login(is_htmx)
    # Invalid/Expired access token scenario
    user_details = decode_access_token(access_token)
    if user_details is None:
        logger.error("Invalid or expired access token provided. Redirecting to login page.")
        set_flash(
            request=request,
            message="Your session has expired. Please login again.",
            category="error"
        )
        return redirect_to_login(is_htmx)
    # Valid access token scenario
    # Add user initials in request state
    initials = f"{user_details.get('first_name', 'U')[0].upper()}{user_details.get('last_name', 'U')[0].upper()}"
    request.state.initials = initials
    # Add user ID in request state
    request.state.user_id = user_details.get("user_id", -1)
    # Create response object and return it
    response = await call_next(request)
    return response


app.add_middleware(SessionMiddleware, secret_key=settings.jwt_secret_key)   # noqa


@app.get("/")
@app.get("/home")
def home_page(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Home page after user is successfully authenticated
    """
    # Retrieve access token from cookies to get user details
    access_token = request.cookies.get("access_token", "")
    user_details = decode_access_token(access_token)
    first_name = user_details.get("first_name", "") if user_details else ""
    greeting = greet_user(first_name)
    # Get today's date
    today_date = datetime.now(tz=IST).date()
    formatted_date = today_date.strftime("%A, %d %B %Y")
    # Get recent daily updates
    recent_work_updates = get_recent_work_updates_for_user(session=db, user_id=request.state.user_id)
    recent_work_updates = [update.to_dict() for update in recent_work_updates]
    # Get flash messages
    flash = get_flash(request=request)
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "greeting": greeting,
            "today_date": formatted_date,
            "name": first_name,
            "recent_work_updates": recent_work_updates,
            "flash": flash
        }
    )
