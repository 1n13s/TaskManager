from fastapi import APIRouter, Header
from starlette import status
from passlib.context import CryptContext
from ApiTaskManager.auth.jwt_create import *
from ApiTaskManager.core.user_manager import UserManager
from ApiTaskManager.core.tasks_manager import TaskManager
from .type_in import AddUserSchemaInput, AddTaskSchemaInput, AuthUserSchemaInput, GetUserTasksSchemaInput
auth = APIRouter()

@auth.post("/get_token")
def get_token(user: AuthUserSchemaInput):
    return write_token(user.dict())

@auth.post("/verify_token")
def validate_token(token:str):
    is_valid = verify_token(token)
    auth_info = read_token(token)
    return UserManager.auth_user(auth_info=auth_info) if is_valid == True else is_valid

@auth.post("/auth_token")
def auth_token(Authorization: str = Header(None)):
    print(Authorization)
    return True