from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db import WorkUpdates, get_db
from src.templates import templates

router = APIRouter(prefix="/filter", tags=["filter"])


@router.get("")
def filter_page(request: Request):
    """
    GET Route to render filter page
    """
    return templates.TemplateResponse(
        request=request,
        name="filter_page.html",
        context={}
    )

@router.post("")
def filter_work_updates(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        user_id: int | None = Form(None),
        topic_id: int | None = Form(None),
        single_date: str | None = Form(None),
        from_date: str | None = Form(None),
        to_date: str | None = Form(None)
):
    """
    POST Route to process work update filtering
    """
    pass
