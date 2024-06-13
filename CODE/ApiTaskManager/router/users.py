from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette import status
from passlib.context import CryptContext
from ApiTaskManager.router.auth import get_access_token
from ApiTaskManager.core.user_manager import UserManager
from .type_in import AddUserSchemaInput, ChangeUserPassword
user = APIRouter(
    prefix="/user",
    tags=["user"]
)

bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

@user.get("/",status_code=status.HTTP_200_OK)
def test_connection():
    """Root"""
    return JSONResponse(content={"message":"Connected successfully"}, status_code=status.HTTP_200_OK)

@user.post("/add", status_code=status.HTTP_201_CREATED)
def add_user(user: AddUserSchemaInput):
    """Add user"""
    return UserManager.add_user(user)

@user.get("/get", status_code= status.HTTP_200_OK)
def get_all_users():
    """Get users
    """
    return UserManager.get_all_users()

@user.put("/update_password", status_code=status.HTTP_200_OK)
def update_password(change_password: ChangeUserPassword, user: dict = Depends(get_access_token)):
    try:
        user_info = UserManager.get_user_id(user_name=user["user_name"])
        return UserManager.change_password(change_password=change_password,  user_id=user_info["user"].id)
    
    except Exception as e:
        JSONResponse(content={"message": f"Getting users has failed {e}"}, status_code=500)