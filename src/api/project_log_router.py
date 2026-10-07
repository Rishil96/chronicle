from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from src.db import get_db
from src.logger import logger
from src.service_layer import get_all_projects, add_project_log, get_project_logs
from src.templates import templates
from src.utils import get_user_id_from_cookie, sort_logs_by_date


# Router object to handle project log functionality
router = APIRouter(prefix="/project-logs", tags=["project-logs"])


@router.get("/new")
def project_log_page(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Page to add a new project log
    """
    all_projects = get_all_projects(session=db)
    return templates.TemplateResponse(
        request=request,
        name="add_project_log.html",
        context={"all_projects": all_projects},
    )


@router.post("")
def new_project_log(request: Request, db: Annotated[Session, Depends(get_db)], project_id: int = Form(), log: str = Form(...)):
    """
    POST route to make a new project log entry
    """
    # Read user ID from cookie
    user_id = get_user_id_from_cookie(request=request)
    # Make database entry
    add_project_log(session=db, user_id=user_id, log=log, project_id=project_id)
    logger.info(f"New project log added. User ID: {user_id} | Project ID: {project_id}")
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("")
def all_project_logs(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Route to view all project logs for the past N days
    """
    # Read project logs for past N days
    past_project_logs = get_project_logs(db)
    past_project_logs = [past_project_log.to_dict() for past_project_log in past_project_logs]
    past_project_logs = sort_logs_by_date(past_project_logs)
    return templates.TemplateResponse(
        request=request,
        name="project_logs.html",
        context={"past_project_logs": past_project_logs}
    )


@router.put("/{project_log_id}")
def edit_project_log(project_log_id: int):
    pass


@router.delete("/{project_log_id}")
def delete_project_log(project_log_id: int):
    pass
