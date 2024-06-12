from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from typing import Dict
from ApiTaskManager.core.user_manager import UserManager
from OpenSSL import rand


SECRET='ge8ZXhERUrmTic6rcHYMKKOc75qbNdiy'
ALGORITHM = 'HS256'

def expire_date() -> datetime:
    """Obtains the expire date

    Returns:
        datetime: The expire date with one day
    """
    date = datetime.now()
    return date + timedelta(days=1)

def write_token(login_info: dict) -> str:
    """Creates the token

    Args:
        login_info (dict): The info of login 

    Returns:
        str: The token with the info
    """
    return encode(payload={**login_info, "exp": expire_date()}, key=SECRET, algorithm=ALGORITHM)

def verify_token(token) -> Dict[str, str]|bool:
    """Verifies a token given

    Args:
        token (any): The token with the login info

    Returns:
        Dict[str, str]|bool: The validation of the decoding or token status
    """
    try: 
        decode(token, key=SECRET, algorithms=ALGORITHM)
        return True
    except exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid Token"}, status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Token Expired"}, status_code=401)
    except Exception as e:
        return JSONResponse(content={"message": f"The auth validation has failed {e}"}, status_code=500)
    
def read_token(token) -> str:
    """Reads and decodes the token

    Args:
        token (any): The token with the login info

    Returns:
        str: The token decoe
    """
    return decode(token, key=SECRET, algorithms=ALGORITHM)

