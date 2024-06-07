import sqlite3
from typing import Dict, List
class UserManager():
    """Manages the Database
    """
    def __init__(self, database: str) -> None:
        """Initializes db"""
        self.__database=database
    
    def insert_user(self, user_info: dict) -> Dict[str, str]:
        """Inserts a user from the info of the user provided

        Args:
            user_info (dict): Info of the user

        Returns:
            Dict[str, str]: The message of the register
        """

        connection=sqlite3.connect(self.__database)
        cursor = connection.cursor()
        query = 'INSERT INTO users (user_name, password) VALUES (?, ?)'
        try:
            cursor.execute(query, (user_info["user_name"], user_info["password"]))
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
        query = """SELECT * FROM users"""
        try:
            cursor.execute(query)
            connection.commit()
            rows = cursor.fetchall()
            users = [
                {"id": row[0], "user_name": row[1], "password": row[2]}
                for row in rows
            ]
            return {"users": users}
        except sqlite3.Error as e:
            print("Getting users has failed", e)

        self.sql_close_connection(connection)

    def sql_close_connection(self, connection: sqlite3.Connection) -> None:
        connection.close()