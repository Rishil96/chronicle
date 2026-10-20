from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from src.config import settings
from src.db import get_db
from src.service_layer import get_all_topics, get_all_users, get_filtered_work_updates, get_work_updates
from src.templates import templates
from src.utils import get_flash, set_flash, sort_work_updates_by_date

router = APIRouter(prefix="/filter", tags=["filter"])


@router.get("")
def filter_page(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    GET Route to render filter page
    """
    # Retrieve all users and topics
    all_users = get_all_users(session=db)
    all_topics = get_all_topics(session=db)
    # Retrieve flash messages
    flash = get_flash(request=request)
    return templates.TemplateResponse(
        request=request,
        name="filter_page.html",
        context={"users": all_users, "topics": all_topics, "flash": flash},
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
    # Case 1: No filters applied
    if not any([user_id, topic_id, single_date, from_date, to_date]):
        updates_list = get_work_updates(session=db)
        updates_list = [update.to_dict() for update in updates_list]
        updates_list = sort_work_updates_by_date(updates_list)
        return templates.TemplateResponse(
            request=request,
            name="_filter_results.html",
            context={
                "updates_list": updates_list,
                "no_filters": True,
                "message": f"No filters applied — showing last {settings.work_update_history_days} day(s) of updates."
            },
        )
    # Case 2: Invalid date range - From Date greater than To Date
    if from_date and to_date and from_date > to_date:
        set_flash(request=request, message="'From Date' cannot be after 'To Date'")
        response = Response(status_code=status.HTTP_200_OK)
        response.headers["HX-Redirect"] = "/filter"
        return response
    # Case 3: Get updates for given filters
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
        context={"updates_list": updates_list, "no_filters": False, "message": ""},
    )
