from fastapi import APIRouter, Depends
from starlette import status
from passlib.context import CryptContext
from ApiTaskManager.auth.jwt_create import *
from ApiTaskManager.core.user_manager import UserManager
from ApiTaskManager.core.tasks_manager import TaskManager
from .type_in import AddUserSchemaInput, AddTaskSchemaInput, AuthUserSchemaInput, GetUserTasksSchemaInput
router = APIRouter()

bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

@router.get("/",status_code=status.HTTP_200_OK)
def test_connection():
    """Root"""
    return {"Message":"You have been connected successfully"}

@router.post("/user_id", status_code=status.HTTP_200_OK)
def get_id(id: int):
    return UserManager.get_user_id(id)

@router.post("/add_user", status_code=status.HTTP_201_CREATED)
def add_user(user: AddUserSchemaInput):
    """Add user"""
    return UserManager.add_user(user)

@router.get("/get-users", status_code= status.HTTP_200_OK)
def get_all_users():
    """Get users
    """
    return UserManager.get_all_users()

@router.post("/add-task", status_code=status.HTTP_201_CREATED)
def add_task(task: AddTaskSchemaInput):
    return TaskManager.insert_task(task)

@router.post("/get-tasks", status_code=status.HTTP_200_OK)
def get_user_tasks(id: GetUserTasksSchemaInput):
    try:
        return TaskManager.get_user_tasks(id.user_id)
    except Exception as e:
        print(f"Error en router{e}")
