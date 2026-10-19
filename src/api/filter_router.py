from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session

from src.db import get_db
from src.service_layer import get_filtered_work_updates
from src.templates import templates
from src.utils import sort_work_updates_by_date

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
    # Parse dates if not None
    single_date = datetime.strptime(single_date, "%Y-%m-%d").date() if isinstance(single_date, str) else None
    from_date = datetime.strptime(from_date, "%Y-%m-%d").date() if isinstance(from_date, str) else None
    to_date = datetime.strptime(to_date, "%Y-%m-%d").date() if isinstance(to_date, str) else None
    # Get filtered updates
    updates_list = get_filtered_work_updates(
        session=db,
        user_id=user_id,
        topic_id=topic_id,
        single_date=single_date,
        from_date=from_date,
        to_date=to_date
    )
    # Convert the updates list into list of dictionaries
    updates_list = [update.to_dict() for update in updates_list]
    updates_list = sort_work_updates_by_date(updates_list)
    return templates.TemplateResponse(
        request=request,
        name="_filter_results.html",
        context={"updates_list": updates_list},
    )
