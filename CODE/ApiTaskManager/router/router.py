from fastapi import APIRouter, Depends
from starlette import status
from passlib.context import CryptContext
from ApiTaskManager.auth.jwt_create import *
from ApiTaskManager.core.user_manager import UserManager
from ApiTaskManager.core.tasks_manager import TaskManager
from .type_in import AddUserSchemaInput, AddTaskSchemaInput, AuthUserSchemaInput, GetUserTasksSchemaInput
router = APIRouter()

bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

def get_user_manager():
    return UserManager()

def get_task_manager():
    return TaskManager()

@router.get("/",status_code=status.HTTP_200_OK)
def test_connection():
    """Root"""
    return {"Message":"You have been connected successfully"}

@router.post("/user_id", status_code=status.HTTP_200_OK)
def get_id(id: int, user_manager: UserManager = Depends(get_user_manager)):
    return user_manager.get_user_id(id)

@router.post("/auth-user")
def auth(auth_info: AuthUserSchemaInput, user_manager: UserManager = Depends(get_user_manager)):
    return user_manager.auth_user(auth_info)

@router.post("/add_user", status_code=status.HTTP_201_CREATED)
def add_user(user: AddUserSchemaInput, user_manager: UserManager = Depends(get_user_manager)):
    """Add user"""
    return user_manager.add_user(user)

@router.get("/get-users", status_code= status.HTTP_200_OK)
def get_all_users(user_manager: UserManager = Depends(get_user_manager)):
    """Get users
    """
    return user_manager.get_all_users()

@router.post("/add-task", status_code=status.HTTP_201_CREATED)
def add_task(task: AddTaskSchemaInput, task_manager: TaskManager = Depends(get_task_manager)):
    return task_manager.insert_task(task)

@router.post("/get-tasks", status_code=status.HTTP_200_OK)
def get_user_tasks(id: GetUserTasksSchemaInput, task_manager: TaskManager = Depends(get_task_manager)):
    try:
        return task_manager.get_user_tasks(id.user_id)
    except Exception as e:
        print(f"Error en router{e}")
