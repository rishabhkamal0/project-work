from fastapi import APIRouter

router = APIRouter()

@router.get("/auth-test")
def auth_test():
    return {"message": "Auth route works!"}
