import logging
from fastapi import APIRouter

router = APIRouter(prefix="/daily-updates", tags=["daily-updates"])
logger = logging.getLogger("chronicle")


@router.get("/new")
def daily_update_page():
    """
    Page to add a new daily update
    """
    pass


@router.post("")
def add_daily_update():
    """
    Route to add a new daily update via HTML form
    """
    pass


@router.get("")
def all_daily_updates():
    """
    Page to view daily updates of colleagues for the past week
    """
    pass


@router.put("/{daily_update_id}")
def edit_daily_update(daily_update_id: int):
    """
    Route to edit a daily update
    """
    pass


@router.delete("/{daily_update_id}")
def delete_daily_update(daily_update_id: int):
    """
    Route to delete a daily update
    """
    pass
