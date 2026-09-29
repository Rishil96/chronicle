from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login")
def login_page():
    pass

@router.post("/login")
def login_user():
    pass

@router.get("/logout")
def logout():
    pass
