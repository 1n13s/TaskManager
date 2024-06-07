from fastapi import APIRouter
from starlette import status
from ApiTaskManager.core.database import Database
from .type_in import AddTaskShemaInput

router = APIRouter()

DB = Database("../../../DATABASE/taskmanager.db")

@router.get("/",status_code=status.HTTP_200_OK)
def get_books():
    """Root"""
    return {"Message":"Hello"}

@router.post("/add_user",status_code=status.HTTP_201_CREATED)
def add_user(task: AddTaskShemaInput):
    """Add user"""
    return DB.insert_user(dict(task))

@router.get("/get-users", status_code= status.HTTP_200_OK)
def  get_users():
    """Get users
    """
    return DB.get_all_users()

