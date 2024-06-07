import sqlite3
from typing import Dict, List
class Database():
    """Manages the Database
    """
    def __init__(self, database: str) -> None:
        """Initializes db"""
        self.__database=database
    @staticmethod
    def sql_connect(database: str) -> sqlite3.Connection:
        """Starts the database connection

        Args:
            database (str): Name of the Database

        Returns:
            sqlite3.Connection: The connection object
        """
        try:
            return sqlite3.connect(database)
        except sqlite3.Error as e:
            print("The database connection has falied", e)
    
    def insert_user(self, user_info: dict) -> Dict[str, str]:
        
        connection=self.sql_connect(self.__database)

        cursor = connection.cursor()

        query = 'INSERT INTO users (user_name, password) VALUES (?, ?)'
        try:
            cursor.execute(query, (user_info["user_name"], user_info["password"]))
            return {"message": "The user has been successfully inserted"}
        except sqlite3.Error as e:
            print("The insert of the user has failed", e)

        connection.commit()

        self.sql_close_connection(connection)
    
    def get_all_users(self) -> Dict[str, List[any]]:
        connection=self.sql_connect(self.__database)
        cursor = connection.cursor()

        query = """SELECT * FROM users"""

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            users = list(rows)
            print(rows)
            return {"users": users}
        except sqlite3.Error as e:
            print("Getting users has failed", e)

        self.sql_close_connection(connection)


    def sql_close_connection(self, connection: sqlite3.Connection) -> None:
        connection.close()