from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import Annotated
from src.db import get_db
from src.service_layer import get_all_projects
from src.templates import templates


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
def new_project_log():
    pass


@router.get("")
def all_project_logs():
    pass


@router.put("/{project_log_id}")
def edit_project_log(project_log_id: int):
    pass


@router.delete("/{project_log_id}")
def delete_project_log(project_log_id: int):
    pass
