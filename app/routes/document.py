from fastapi import APIRouter

router = APIRouter()

@router.get("/document-test")
def document_test():
    return {"message": "Document route works!"}
