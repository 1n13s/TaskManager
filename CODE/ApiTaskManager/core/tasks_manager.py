import sqlite3
from typing import Dict, List
class TaskManager():
    """Manages the Tasks in the Database
    """
    def __init__(self, database: str) -> None:
        """Initializes the task manager"""
        self.__database=database
        self.___table="tasks"

    def insert_user(self, user_info: dict) -> Dict[str, str]:
        """Inserts a user from the info of the user provided

        Args:
            user_info (dict): Info of the user

        Returns:
            Dict[str, str]: The message of the register
        """

        connection=sqlite3.connect(self.__database)
        cursor = connection.cursor()
        query = f'INSERT INTO {self.__table} (email, user_name, first_name, last_name, hashed_password, is_active) VALUES (?, ?, ?, ?, ?, ?)'
        try:
            cursor.execute(query, 
                           (
                                user_info["email"], 
                                user_info["user_name"], 
                                user_info["first_name"], 
                                user_info["last_name"], 
                                user_info["hashed_password"], 
                                user_info["is_active"]
                            ))
            connection.commit()
            row_count = cursor.rowcount
            if row_count > 0:
                return {"message": "The user has been successfully inserted"}
            else:
                return {"message": "Failed to insert user"}
           
        except sqlite3.Error as e:
            return {"message": f"The insert of the user has failed: {e}"}
        
        finally:
            self.sql_close_connection(connection)
    
    def get_all_users(self) -> Dict[str, List[any]]:
        connection=sqlite3.connect("../DATABASE/taskmanager.db")
        cursor = connection.cursor()
        query = f"SELECT * FROM {self.__table}"
        try:
            cursor.execute(query)
            connection.commit()
            rows = cursor.fetchall()
            users = [
                {
                    "id": row[0],
                    "email": row[1],
                    "user_name": row[2],
                    "first_name": row[3],
                    "last_name": row[4],
                    "hashed_password": row[5],
                    "is_active": row[6]
                }
                for row in rows
            ]
            return {"users": users}
        except sqlite3.Error as e:
            print("Getting users has failed", e)

        self.sql_close_connection(connection)

    def sql_close_connection(self, connection: sqlite3.Connection) -> None:
        connection.close()