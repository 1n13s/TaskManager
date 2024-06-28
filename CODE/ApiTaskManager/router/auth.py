from fastapi import APIRouter, Header, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWSError
from typing import Optional, Annotated
from fastapi.templating import Jinja2Templates

from ApiTaskManager.auth.jwt_create import *
from ApiTaskManager.core.user_manager import UserManager
from ApiTaskManager.core.tasks_manager import TaskManager
from ApiTaskManager.router.type_in import Token, AuthUserSchemaInput
from .type_in import AddUserSchemaInput, AddTaskSchemaInput, AuthUserSchemaInput

auth = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET = 'ge8ZXhERUrmTic6rcHYMKKOc75qbNdiy'
ALGORITHM = 'HS256'

templates = Jinja2Templates(directory="template")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def create_access_token(login_info: dict, expires_delta: timedelta) -> str:
    """Creates the token

    Args:
        login_info (dict): The info of login 
        expires_delta (timedelta): The time to espires

    Returns:
        str: The token with the info
    """
    return jwt.encode({**login_info, "exp": datetime.now(timezone.utc) + expires_delta}, key=SECRET, algorithm=ALGORITHM)

def get_access_token(token: str = Depends(oauth2_bearer)) -> Dict[str, str]:
    """try:
        
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        print (payload)
        print(type(payload))
    except Exception as e:
        print(e)"""
    
    try: 
        return jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid Token"}, status_code=status.HTTP_401_UNAUTHORIZED)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Token Expired"}, status_code=status.HTTP_401_UNAUTHORIZED)
    except JWSError:
        JSONResponse(
            content={"message": "Could not validate user"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    except Exception as e:
        return JSONResponse(content={"message": f"The auth validation has failed {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

#@auth.post("/token")
def obtain_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    auth_info = AuthUserSchemaInput(user_name=form_data.username, hashed_password=form_data.password)
    user_auth = UserManager.auth_user(auth_info=auth_info.dict())
    if user_auth !=True:
        return user_auth
    token = create_access_token(auth_info.dict(), timedelta(minutes=20))
    
    return {"access_token": token, "token_type": "bearer"}

@auth.post("/login")
async def login(request: Request, token: dict = Depends(obtain_access_token)):
    if "access_token" not in token.keys():
        response = RedirectResponse("/taskmanager/login", status_code=status.HTTP_302_FOUND)
    else: 
        #response = JSONResponse(content={"message": "Successfully logged in"})
        response = RedirectResponse("/taskmanager/main_page", status_code=status.HTTP_302_FOUND)
        cookie_params = {
            "key": "access_token",
            "value": token['access_token'],
            "httponly": True
        }
        
        response.set_cookie(**cookie_params)
        
    return response
    #response.set_cookie(key="auth_token",value=token, httponly=True)

