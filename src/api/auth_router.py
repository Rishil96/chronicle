from fastapi import APIRouter, Request
from src.templates import templates

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
def login_user():
    pass

@router.get("/logout")
def logout():
    pass
