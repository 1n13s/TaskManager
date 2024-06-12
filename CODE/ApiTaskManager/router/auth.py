from fastapi import APIRouter, Header
from starlette import status
from passlib.context import CryptContext
from ApiTaskManager.auth.jwt_create import *
from ApiTaskManager.core.user_manager import UserManager
from ApiTaskManager.core.tasks_manager import TaskManager
from .type_in import AddUserSchemaInput, AddTaskSchemaInput, AuthUserSchemaInput
auth = APIRouter()

@auth.post("/get_token")
def get_token(user: AuthUserSchemaInput):
    return JSONResponse(content={"token":write_token(user.dict())})
