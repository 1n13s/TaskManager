from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette import status
from passlib.context import CryptContext
from ApiTaskManager.router.auth import get_access_token
from ApiTaskManager.core.user_manager import UserManager
from ApiTaskManager.core.tasks_manager import TaskManager
from .type_in import AddTaskSchemaInput, UseTaskIdSchemaInput, UpdateTaskShemaInput, UpdateTaskStateInput

task = APIRouter(
    prefix="/task",
    tags=["task"]
)

bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

@task.post("/add", status_code=status.HTTP_201_CREATED)
def add_task(task: AddTaskSchemaInput, user: dict = Depends(get_access_token)):
    
    user_info = UserManager.get_user_id(user_name=user["user_name"])
    return TaskManager.insert_task(task_info=task, user_id=user_info["user"].id)

@task.post("/get", status_code=status.HTTP_200_OK)
def get_user_tasks_auth(user: dict = Depends(get_access_token)):
    try:    
        if user is None:
            raise JSONResponse(content={"message": "The user is not valid"})
        
        user_info = UserManager.get_user_id(user_name=user["user_name"])
        return TaskManager.get_user_tasks(user_info["user"].id)
    except Exception as e:
        JSONResponse(content={"message": f"Getting users has failed {e}"}, status_code=500)

@task.delete("/delete", status_code=status.HTTP_200_OK)
def delete_task(id_task: UseTaskIdSchemaInput, user: dict = Depends(get_access_token)):
    try:
        user_info = UserManager.get_user_id(user_name=user["user_name"])

        return TaskManager.delete_task(user_id=user_info["user"].id, task_id=id_task.id_task)
    except Exception as e:
        JSONResponse(content={"message": f"Getting users has failed {e}"}, status_code=500)

@task.put("/update", status_code=status.HTTP_200_OK)
def update_task(task: UpdateTaskShemaInput, user: dict = Depends(get_access_token)):
    try:
        user_info = UserManager.get_user_id(user_name=user["user_name"])
        return TaskManager.update_tasks(task_info=task, user_id=user_info["user"].id)
    except Exception as e:
        JSONResponse(content={"message": f"Getting users has failed {e}"}, status_code=500)

@task.put("/update_state", status_code=status.HTTP_200_OK)
def update_state(task: UpdateTaskStateInput, user: dict = Depends(get_access_token)):
    try:
        user_info = UserManager.get_user_id(user_name=user["user_name"])
        return TaskManager.update_task_state(
            user_id=user_info["user"].id,
            task_id=task.id_task,
            state=task.complete
        )
    
    except Exception as e:
        JSONResponse(content={"message": f"Getting users has failed {e}"}, status_code=500)
