import sqlite3
from typing import Dict, List
from .user_manager import UserManager
from ..database.connection import session, Base, engine
from ..database.models import Tasks
from ..router.type_in import AddTaskSchemaInput


class TaskManager():
    """Manages the Tasks in the Database
    """
    def __init__(self, database: str) -> None:
        """Initializes the task manager"""
        self.__db__=session()

    def insert_task(self, task_info: AddTaskSchemaInput) -> Dict[str, str]:
        """Inserts a user from the info of the user provided

        Args:
            user_info (dict): Info of the user

        Returns:
            Dict[str, str]: The message of the register
        """

        try:
            user=UserManager()
            if not user.get_user_id(task_info.id_user):
                return {"message": "There is not any user with this id"}
            new_task = Tasks(**task_info.dict())
            self.__db__.add(new_task)
            self.__db__.commit()

            return {"message": "The task has been successfully inserted"}
        
        except Exception as e:
            return {"message": f"The insert of the task has failed: {e}"}
        
        finally:
            self.__db__.close()
    
    def get_user_tasks(self, user_id: int) -> Dict[str, List[any]]:
        """Gets all tasks

        Returns:
            Dict[str, List[any]]: Tasks info
        """

        try:
           return {"tasks": self.__db__.query(Tasks).filter(Tasks.id_user==user_id).all()}

        except Exception as e:
           return{"message": f"Getting users has failed {e}"}

        finally:
            self.__db__.close()