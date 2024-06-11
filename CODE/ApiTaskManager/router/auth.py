from fastapi import APIRouter, Depends
from starlette import status
from passlib.context import CryptContext
from ApiTaskManager.auth.jwt_create import *
from ApiTaskManager.core.user_manager import UserManager
from ApiTaskManager.core.tasks_manager import TaskManager
from .type_in import AddUserSchemaInput, AddTaskSchemaInput, AuthUserSchemaInput, GetUserTasksSchemaInput
auth = APIRouter()

def get_user_manager():
    return UserManager()

def get_task_manager():
    return TaskManager()

@auth.post("/get_token")
def get_token(user: AuthUserSchemaInput):
    return write_token(user.dict())

@auth.post("/verify_token")
def validate_token(token:str):
    um=UserManager()
    is_valid = verify_token(token)
    auth_info = read_token(token)
    return um.auth_user(auth_info=auth_info) if is_valid == True else is_valid
