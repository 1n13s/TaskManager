from fastapi import APIRouter, Depends, Header
from typing import Dict, List
from starlette import status
from passlib.context import CryptContext
from ApiTaskManager.auth.jwt_create import *
from ApiTaskManager.core.user_manager import UserManager
from ApiTaskManager.core.tasks_manager import TaskManager
from .type_in import AddUserSchemaInput, AddTaskSchemaInput, DeleteTaskSchemaInput
router = APIRouter()

bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

def valid_tocken(autorization: str) -> Dict[str, str]|bool:
    """Validates if the token is valid

    Args:
        autorization (str): The authorization token

    Returns:
        bool|Dict[str, str]: Validates if the token is valid or why not
    """
    auth = autorization.split(" ")
    return verify_token(auth[1])

def valid_authorization(token: str) -> Dict[str,str]|bool:
    """Validates if the user has autorization

    Args:
        token (str): The token to auth

    Returns:
        Dict[str,str]|bool: Validates if the user has autorization
    """
    return UserManager.auth_user(auth_info=read_token(token))    

@router.get("/",status_code=status.HTTP_200_OK)
def test_connection():
    """Root"""
    return {"Message":"You have been connected successfully"}

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
def add_task(task: AddTaskSchemaInput, Authorization: str = Header(None)):
    auth = Authorization.split(" ")
    token = auth[1]

    is_valid = valid_tocken(Authorization)
    
    if is_valid != True:
        return is_valid
    
    user_validation = valid_authorization(token)

    if user_validation != True:
        return user_validation
    
    auth_info = read_token(token)
    user = UserManager.get_user_id(user_name=auth_info["user_name"])
    task.id_user = user["user"].id

    return TaskManager.insert_task(task)

@router.post("/get-tasks", status_code=status.HTTP_200_OK)
def get_user_tasks(Authorization: str = Header(None)):
    try:
        auth = Authorization.split(" ")
        token = auth[1]

        is_valid = valid_tocken(Authorization)
    
        if is_valid != True:
            return is_valid
        
        user_validation = valid_authorization(token)

        if user_validation != True:
            return user_validation
        
        auth_info = read_token(token)
        user = UserManager.get_user_id(user_name=auth_info["user_name"])

        return TaskManager.get_user_tasks(user["user"].id)
    except Exception as e:
        JSONResponse(content={"message": f"Getting users has failed {e}"}, status_code=500)

@router.delete("/delete-task", status_code=status.HTTP_200_OK)
def delete_task(id_task: DeleteTaskSchemaInput, Authorization: str = Header(None)):
    try:
        auth = Authorization.split(" ")
        token = auth[1]

        is_valid = valid_tocken(Authorization)
    
        if is_valid != True:
            return is_valid
        
        user_validation = valid_authorization(token)

        if user_validation != True:
            return user_validation
        
        auth_info = read_token(token)
        user = UserManager.get_user_id(user_name=auth_info["user_name"])

        return TaskManager.delete_task(user_id=user["user"].id, task_id=id_task.id_task)
    except Exception as e:
        JSONResponse(content={"message": f"Getting users has failed {e}"}, status_code=500)
