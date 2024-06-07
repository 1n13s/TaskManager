from fastapi import APIRouter, Depends
from starlette import status
from ApiTaskManager.core.user_manager import UserManager
from ApiTaskManager.core.tasks_manager import TaskManager
from .type_in import AddUserSchemaInput, AddTaskSchemaInput

router = APIRouter()

def get_user_manager():
    return UserManager("../DATABASE/taskmanager.db")

def get_task_manager():
    return TaskManager("../DATABASE/taskmanager.db")

@router.get("/",status_code=status.HTTP_200_OK)
def test_connection():
    """Root"""
    return {"Message":"Connection Succesfully"}

@router.post("/add_user", status_code=status.HTTP_201_CREATED)
def add_user(user: AddUserSchemaInput, user_manager: UserManager = Depends(get_user_manager)):
    """Add user"""
    return user_manager.insert_user(dict(user))

@router.get("/get-users", status_code= status.HTTP_200_OK)
def get_all_users(user_manager: UserManager = Depends(get_user_manager)):
    """Get users
    """
    return user_manager.get_all_users()

@router.post("/add-task", status_code=status.HTTP_201_CREATED)
def add_task(task: AddTaskSchemaInput, task_manager: TaskManager = Depends(get_task_manager)):
    return task_manager.insert_task(dict(task))

@router.get("/get-task", status_code=status.HTTP_200_OK)
def get_all_tasks(task_manager: TaskManager = Depends(get_task_manager)):
    return task_manager.get_all_tasks()
