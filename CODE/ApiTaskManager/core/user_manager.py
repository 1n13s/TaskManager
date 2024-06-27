from fastapi.responses import JSONResponse
from typing import Dict, List
from passlib.context import CryptContext
from ..database.connection import session, Base, engine
from ..database.models import Users
from ..router.type_in import AddUserSchemaInput, ChangeUserPassword

bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")
Base.metadata.create_all(bind=engine)

class UserManager():
    """Manages the Users in the Database
    """
    @staticmethod
    def add_user(user_info: AddUserSchemaInput) -> Dict[str, str]:
        """Adds an user from the info of the user provided

        Args:
            user_info (AddUserSchemaInput): Info of the user

        Returns:
            Dict[str, str]: The message of the register
        """

        try:
            if not UserManager.validate_user_name(user_info.user_name):
                return JSONResponse(content={"message": "This user name has been repeated"})
            
            user_info.hashed_password = bcrypt_context.hash(user_info.hashed_password)
            new_user = Users(**user_info.dict())
            db=session()
            db.add(new_user)
            db.commit()
            return JSONResponse(content={"message": "This user has been added successfully"})
           
        except Exception as e:
            return JSONResponse(content={"message": f"The insert of the user has failed: {e}"})
        
        finally:
            db.close()
    
    @staticmethod
    def get_user_id(user_id: int = None, user_name: str = None) -> Dict[str, any]:
        """Gets an user by an id

        Args:
            id (int): Id to find

        Returns:
            Dict[str, any]: The info of the user or False if there is not an user with this id
        """

        try:
            db=session()
            if not user_id: user = db.query(Users).filter(Users.user_name==user_name).first()
            else: user = db.query(Users).filter(Users.id==user_id).first()
            return {"user": user} if user else False
        except Exception as e:
            return JSONResponse(content={"message": f"The find of the user has failed: {e}"}, status_code=500)

        finally:
            db.close()
    
    @staticmethod
    def get_all_users() -> Dict[str, List[any]]:
        """Gets all users in the database

        Returns:
            Dict[str, List[any]]: The users info
        """

        try:
            db=session()
            return {"users": db.query(Users).all()}
        
        except Exception as e:
            return JSONResponse({"message": f"Getting users has failed {e}"})

        finally:
            db.close()
    
    @staticmethod
    def auth_user(auth_info: dict) -> Dict[str, str]:
        """Authenticates an user

        Args:
            auth_info (dict): The info of the user that wants to authenticated

        Returns:
            Dict[str, str]: If the user has authenticated successfully
        """

        try:
            db=session()
            if (
                user := db.query(Users)
                .filter(Users.user_name == auth_info["user_name"])
                .first()
            ):
                if bcrypt_context.verify(auth_info["hashed_password"], user.hashed_password):
                    return True
                else:
                    return {"message":"The password is incorrect"}

            else:
                return {"message":"The user name does not exist"}
        
        except Exception as e:
            return {"message": f"Auth user has failed {e}"}

        finally:
            db.close()

    @staticmethod
    def change_password(change_password: ChangeUserPassword, user_id: int):
        db = session()
        try:
            user_to_update = db.query(Users).filter(Users.id==user_id).first()

            if not user_to_update:
                return JSONResponse(content={"message": "The user does not exist"}, status_code=404)

            if not bcrypt_context.verify(change_password.current_password, user_to_update.hashed_password):
                return JSONResponse(content={"message": "The password is incorrect"}, status_code=401)
            
            if bcrypt_context.verify(change_password.new_password, user_to_update.hashed_password):
                return JSONResponse(content={"message": "The new password should be different to the current password"}, status_code=401)

            user_to_update.hashed_password = bcrypt_context.hash(change_password.new_password)
            db.commit()

            return JSONResponse(content={"message": "Tha password has been changed successfully"})
           
        except Exception as e:
            return JSONResponse(content={"message": f"The change of the password has failed: {e}"}, status_code=500)
        
        finally:
            db.close()

    @staticmethod
    def validate_user_name(user_name: str) -> bool:
        """Validates if the user_name is repeated

        Args:
            user_name (str): The user name

        Returns:
            bool: The user name validation
        """
        try:
            db=session()
            return not db.query(Users).filter(Users.user_name==user_name).first()
        except Exception as e:
            return JSONResponse(content={"message": f"The find of the user has failed: {e}"})
        finally:
            db.close()
