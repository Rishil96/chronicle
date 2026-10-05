from fastapi import APIRouter


# Router object to handle project log functionality
router = APIRouter(prefix="/project-logs", tags=["project-logs"])


@router.get("/new")
def project_log_page():
    pass


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
