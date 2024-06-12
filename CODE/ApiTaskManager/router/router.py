from fastapi import APIRouter, Depends, Header
from typing import Dict, List
from starlette import status
from passlib.context import CryptContext
from ApiTaskManager.router.auth import get_access_token
from ApiTaskManager.auth.jwt_create import *
from ApiTaskManager.core.user_manager import UserManager
from ApiTaskManager.core.tasks_manager import TaskManager
from .type_in import AddUserSchemaInput, AddTaskSchemaInput, DeleteTaskSchemaInput, UpdateTaskShemaInput
router = APIRouter()

bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

@router.get("/",status_code=status.HTTP_200_OK)
def test_connection():
    """Root"""
    return JSONResponse(content={"message":"Connected successfully"}, status_code=status.HTTP_200_OK)

@router.post("/add_user", status_code=status.HTTP_201_CREATED)
def add_user(user: AddUserSchemaInput):
    """Add user"""
    return UserManager.add_user(user)

@router.get("/get_users", status_code= status.HTTP_200_OK)
def get_all_users():
    """Get users
    """
    return UserManager.get_all_users()

@router.post("/add_task", status_code=status.HTTP_201_CREATED)
def add_task(task: AddTaskSchemaInput, user: dict = Depends(get_access_token)):
    
    user_info = UserManager.get_user_id(user_name=user["user_name"])
    return TaskManager.insert_task(task_info=task, user_id=user_info["user"].id)

@router.post("/get_tasks", status_code=status.HTTP_200_OK)
def get_user_tasks_auth(user: dict = Depends(get_access_token)):
    try:    
        if user is None:
            raise JSONResponse(content={"message": "The user is not valid"})
        
        user_info = UserManager.get_user_id(user_name=user["user_name"])
        return TaskManager.get_user_tasks(user_info["user"].id)
    except Exception as e:
        JSONResponse(content={"message": f"Getting users has failed {e}"}, status_code=500)

@router.delete("/delete_task", status_code=status.HTTP_200_OK)
def delete_task(id_task: DeleteTaskSchemaInput, user: dict = Depends(get_access_token)):
    try:
        user_info = UserManager.get_user_id(user_name=user["user_name"])

        return TaskManager.delete_task(user_id=user_info["user"].id, task_id=id_task.id_task)
    except Exception as e:
        JSONResponse(content={"message": f"Getting users has failed {e}"}, status_code=500)

@router.put("/update_task", status_code=status.HTTP_200_OK)
def update_task(task: UpdateTaskShemaInput, user: dict = Depends(get_access_token)):
    try:
        user_info = UserManager.get_user_id(user_name=user["user_name"])
        return TaskManager.update_tasks(task_info=task, user_id=user_info["user"].id)
    except Exception as e:
        JSONResponse(content={"message": f"Getting users has failed {e}"}, status_code=500)

