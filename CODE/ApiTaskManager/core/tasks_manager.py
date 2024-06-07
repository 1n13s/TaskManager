import sqlite3
from typing import Dict, List
from .user_manager import UserManager
class TaskManager():
    """Manages the Tasks in the Database
    """
    def __init__(self, database: str) -> None:
        """Initializes the task manager"""
        self.__database=database
        self.__table="tasks"

    def insert_task(self, task_info: dict) -> Dict[str, str]:
        """Inserts a user from the info of the user provided

        Args:
            user_info (dict): Info of the user

        Returns:
            Dict[str, str]: The message of the register
        """

        connection=sqlite3.connect(self.__database)
        cursor = connection.cursor()
        user=UserManager(self.__database)
        if not user.get_user_id(task_info["id_user"]):
            return {"message": "There is not any user with this id"}

        query = f'INSERT INTO {self.__table} (description, priority, title, complete, id_user) VALUES (?, ?, ?, ?, ?)'
        try:
            cursor.execute(query, 
                        (
                                task_info["description"], 
                                task_info["priority"], 
                                task_info["title"], 
                                task_info["complete"], 
                                task_info["id_user"]
                            ))
            connection.commit()
            row_count = cursor.rowcount
            if row_count > 0:
                return {"message": "The task has been successfully inserted"}
            else:
                return {"message": "Failed to insert task"}
           
        except sqlite3.Error as e:
            return {"message": f"The insert of the task has failed: {e}"}
        
        finally:
            self.sql_close_connection(connection)
    
    def get_all_tasks(self) -> Dict[str, List[any]]:
        connection=sqlite3.connect(self.__database)
        cursor = connection.cursor()
        query = f"SELECT * FROM {self.__table}"
        try:
            cursor.execute(query)
            connection.commit()
            rows = cursor.fetchall()
            return {"tasks": self.get_task_output_format(rows)}

        except sqlite3.Error as e:
            print("Getting users has failed", e)

        self.sql_close_connection(connection)

    def sql_close_connection(self, connection: sqlite3.Connection) -> None:
        connection.close()

    @staticmethod
    def get_task_output_format(rows: list) -> List[Dict[str,any]]:
        return [
                {
                    "id": row[0],
                    "description": row[1],
                    "priority": row[2],
                    "title": row[3],
                    "complete": row[4],
                    "id_user": row[5]
                }
                for row in rows
            ]