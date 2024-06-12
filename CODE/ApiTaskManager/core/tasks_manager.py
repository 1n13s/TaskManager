from fastapi.responses import JSONResponse
from fastapi import HTTPException
from typing import Dict, List
from .user_manager import UserManager
from ..database.connection import session, Base, engine
from ..database.models import Tasks
from ..router.type_in import AddTaskSchemaInput

class TaskManager:
    """Manages the Tasks in the Database"""
    
    @staticmethod
    def insert_task(task_info: AddTaskSchemaInput) -> JSONResponse:
        """Inserts a task from the info provided

        Args:
            task_info (AddTaskSchemaInput): Info of the task

        Returns:
            Dict[str, str]: The message of the register
        """
        db = session()
        try:
            user = UserManager()
            if not user.get_user_id(user_id=task_info.id_user):
                return JSONResponse(content={"message": "This user id has not exist"}, status_code=404)
            
            new_task = Tasks(**task_info.dict())
            db.add(new_task)
            db.commit()

            return JSONResponse(content={"message": "The task has been successfully inserted"})
        
        except Exception as e:
            return JSONResponse(content={"message": f"The insert of the task has failed: {e}"}, status_code=500)
        
        finally:
            db.close()
    
    @staticmethod
    def delete_task(user_id: int, task_id: int) -> JSONResponse:
        """Deletes a task

        Args:
            user_id (int): The id of the user
            task_id (int): The id of the task

        Returns:
            JSONResponse: The message to delete status
        """
        db = session()
        try:
            
            task_to_delete = db.query(Tasks).filter(Tasks.id == task_id).first()

            if not task_to_delete:
                return JSONResponse(content={"message": "The task does not exist"}, status_code=404)

            if not TaskManager.validate_user_id(task_id=task_id, user_id=user_id):
                return JSONResponse(content={"message": "User not authorizated"}, status_code=401)
                        
            db.delete(task_to_delete)
            db.commit()
            return JSONResponse(content={"message": "The task has been deleted"})
        
        except Exception as e:
            return JSONResponse(content={"message": f"Deleting the task has failed: {e}"}, status_code=500)
        
        finally:
            db.close()
    
    @staticmethod
    def get_user_tasks(user_id: int) -> Dict[str, List[any]]|JSONResponse:
        """Gets all tasks for a user

        Args:
            user_id (int): The id of the user

        Returns:
            Dict[str, List[any]]: Tasks info
        """
        db = session()
        try:
            tasks = db.query(Tasks).filter(Tasks.id_user == user_id).all()
            return {"tasks": tasks}
        
        except Exception as e:
            return JSONResponse(content={"message": f"Getting tasks has failed: {e}"}, status_code=500)
        
        finally:
            db.close()
    
    @staticmethod
    def validate_user_id(task_id: int, user_id: int) -> bool:
        """Validates if the user has access to a task

        Args:
            task_id (int): The id of the task
            user_id (int): The id of the user

        Returns:
            bool: The validation result
        """
        db = session()
        try:
            task = db.query(Tasks).filter(Tasks.id == task_id, Tasks.id_user == user_id).first()
            return bool(task)
        
        finally:
            db.close()
