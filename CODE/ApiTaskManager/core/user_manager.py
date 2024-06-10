import sqlite3
from typing import Dict, List
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")


class UserManager():
    """Manages the Users in the Database
    """
    def __init__(self, database: str) -> None:
        """Initializes db"""
        self.__database=database
        self.__table="users"

    def insert_user(self, user_info: dict) -> Dict[str, str]:
        """Inserts a user from the info of the user provided

        Args:
            user_info (dict): Info of the user

        Returns:
            Dict[str, str]: The message of the register
        """

        try:
            connection=sqlite3.connect(self.__database)
            cursor = connection.cursor()
            
            if not self.validate_user_name(user_info["user_name"]):
                return {"message": "This user name has been repeated"}
            
            query = f'INSERT INTO {self.__table} (email, user_name, first_name, last_name, hashed_password, is_active) VALUES (?, ?, ?, ?, ?, ?)'
            cursor.execute(query, 
                        (
                                user_info["email"], 
                                user_info["user_name"], 
                                user_info["first_name"], 
                                user_info["last_name"], 
                                bcrypt_context.hash(user_info["hashed_password"]), 
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
    
    def get_user_id(self, id: int) -> Dict[str, any]|bool:
        """Gets an user by an id

        Args:
            id (int): Id to find

        Returns:
            Dict[str, any]|bool: The info of the user or False if there is not an user with this id
        """

        try:
            connection=sqlite3.connect(self.__database)
            cursor = connection.cursor()
            query = f"SELECT * FROM {self.__table} WHERE id = {id}"
            cursor.execute(query)
            connection.commit()
            rows = cursor.fetchall()
            return False if len(rows) <= 0 else {"user": self.get_user_output_format(rows)}
        
        except sqlite3.Error as e:
            self.sql_close_connection(connection)
            return {"message": f"The find of the user has failed: {e}"}
    
    def get_all_users(self) -> Dict[str, List[any]]:
        """Gets all users in the database

        Returns:
            Dict[str, List[any]]: The users info
        """

        try:
            connection=sqlite3.connect(self.__database)
            cursor = connection.cursor()
            query = f"SELECT * FROM {self.__table}"
            cursor.execute(query)
            connection.commit()
            rows = cursor.fetchall()
            self.sql_close_connection(connection)
            return {"users": self.get_user_output_format(rows)}
        
        except sqlite3.Error as e:
            return {"message": f"Getting users has failed {e}"}

    def auth_user(self, auth_info: dict) -> Dict[str, str]:
        """Authenticates an user

        Args:
            auth_info (dict): The info of the user that wants to authenticated

        Returns:
            Dict[str, str]: If the user has authenticated successfully
        """

        try:
            connection=sqlite3.connect(self.__database)
            cursor = connection.cursor()
            query = f'SELECT * FROM {self.__table} WHERE user_name="{auth_info["user_name"]}"'
            print(query)
            cursor.execute(query)
            connection.commit()
            rows = list(cursor.fetchall())
            user = self.get_user_output_format(rows)
            self.sql_close_connection(connection)
            if bcrypt_context.verify(auth_info["hashed_password"] ,user[0]["hashed_password"]):
                return {"message":"You have been authenticated successfully"}
            else:
                return {"message":"The user_name or password is incorrect"}
        except sqlite3.Error as e:
            return {"message": f"Auth user has failed {e}"}

    def validate_user_name(self, user_name: str) -> bool:
        """Validates if the user_name is repeated

        Args:
            user_name (str): The user name

        Returns:
            bool: The user name validation
        """
        try:
            connection=sqlite3.connect(self.__database)
            cursor = connection.cursor()
            query = f'SELECT * FROM {self.__table} WHERE user_name = "{user_name}"'
            cursor.execute(query)
            connection.commit()
            rows = cursor.fetchall()
            return len(rows) == 0
        
        except sqlite3.Error as e:
            self.sql_close_connection(connection)
            return {"message": f"The find of the user has failed: {e}"}
    
    def sql_close_connection(self, connection: sqlite3.Connection) -> None:
        """Closes the connection

        Args:
            connection (sqlite3.Connection): The connection to close
        """
        connection.close()

    @staticmethod
    def get_user_output_format(rows: list) -> List[Dict[str, any]]:
        """Gets tha output user format

        Args:
            rows (list): The rows obtained in the query

        Returns:
            List[Dict[str, any]]: The list with te right format
        """
        return [
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
