from fastapi.responses import JSONResponse
from typing import Dict, List
from .user_manager import UserManager
from ..database.connection import session, Base, engine
from ..database.models import Tasks
from ..router.type_in import AddTaskSchemaInput


class TaskManager():
    """Manages the Tasks in the Database
    """
    @staticmethod
    def insert_task(task_info: AddTaskSchemaInput) -> Dict[str, str]:
        """Inserts a user from the info of the user provided

        Args:
            user_info (dict): Info of the user

        Returns:
            Dict[str, str]: The message of the register
        """

        try:
            db=session()
            user=UserManager()
            if not user.get_user_id(task_info.id_user):
                return JSONResponse(content={"message": "There is not any user with this id"}, status_code=406)
            
            new_task = Tasks(**task_info.dict())
            db.add(new_task)
            db.commit()

            return JSONResponse(content={"message": "The task has been successfully inserted"})
        
        except Exception as e:
            return JSONResponse(content={"message": f"The insert of the task has failed: {e}"}, status_code=500)
        
        finally:
            db.close()
    
    @staticmethod
    def get_user_tasks(user_id: int) -> Dict[str, List[any]]:
        """Gets all tasks

        Returns:
            Dict[str, List[any]]: Tasks info
        """

        try:
            db=session()
            return {"tasks": db.query(Tasks).filter(Tasks.id_user==user_id).all()}
        
        except Exception as e:
           return JSONResponse(content={"message": f"Getting users has failed {e}"}, status_code=500)

        finally:
            db.close()