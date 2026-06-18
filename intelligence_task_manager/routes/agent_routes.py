from fastapi import APIRouter

router = APIRouter()



@router.get("/")
def heelo():
    return "hello"
