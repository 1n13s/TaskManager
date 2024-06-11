import sqlite3
from typing import Dict, List
from passlib.context import CryptContext
from ..database.connection import session, Base, engine
from ..database.models import Users
from ..router.type_in import AddUserSchemaInput, AuthUserSchemaInput

bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")
Base.metadata.create_all(bind=engine)

class UserManager():
    """Manages the Users in the Database
    """
    def __init__(self) -> None:
        """Initializes db"""
        try:
            self.__db__=session()
        except Exception as e:
            return e

    def add_user(self, user_info: AddUserSchemaInput) -> Dict[str, str]:
        """Adds an user from the info of the user provided

        Args:
            user_info (AddUserSchemaInput): Info of the user

        Returns:
            Dict[str, str]: The message of the register
        """

        try:
            if not self.validate_user_name(user_info.user_name):
                return {"message": "This user name has been repeated"}
            
            user_info.hashed_password=bcrypt_context.hash(user_info.hashed_password)
            new_user = Users(**user_info.dict())
            self.__db__.add(new_user)
            self.__db__.commit()
            return {"message": "This user has been added successfully"}
           
        except Exception as e:
            return {"message": f"The insert of the user has failed: {e}"}
        
        finally:
            self.__db__.close()
    
    def get_user_id(self, id: int) -> Dict[str, any]:
        """Gets an user by an id

        Args:
            id (int): Id to find

        Returns:
            Dict[str, any]: The info of the user or False if there is not an user with this id
        """

        try:
            return {"users": self.__db__.query(Users).filter(Users.id==id).all()}
        
        except Exception as e:
            return {"message": f"The find of the user has failed: {e}"}
        
        finally:
            self.__db__.close()
    
    def get_all_users(self) -> Dict[str, List[any]]:
        """Gets all users in the database

        Returns:
            Dict[str, List[any]]: The users info
        """

        try:
            return {"users": self.__db__.query(Users).all()}
        
        except Exception as e:
            return {"message": f"Getting users has failed {e}"}

        finally:
            self.__db__.close()
    
    def auth_user(self, auth_info: AuthUserSchemaInput) -> Dict[str, str]:
        """Authenticates an user

        Args:
            auth_info (dict): The info of the user that wants to authenticated

        Returns:
            Dict[str, str]: If the user has authenticated successfully
        """

        try:
            if (
                user := self.__db__.query(Users)
                .filter(Users.user_name == auth_info.user_name)
                .first()
            ):
                if bcrypt_context.verify(auth_info.hashed_password ,user.hashed_password):
                    return {"message":"You have been authenticated successfully"}
                else:
                    return {"message":"The password is incorrect"}

            else:
                return {"message":"The user name does not exist"}
        
        except Exception as e:
            return {"message": f"Auth user has failed {e}"}

        finally:
            self.__db__.close()

    def validate_user_name(self, user_name: str) -> bool:
        """Validates if the user_name is repeated

        Args:
            user_name (str): The user name

        Returns:
            bool: The user name validation
        """
        try:
            return not self.__db__.query(Users).filter(Users.user_name==user_name).first()
        except sqlite3.Error as e:
            return {"message": f"The find of the user has failed: {e}"}
        finally:
            self.__db__.close()
