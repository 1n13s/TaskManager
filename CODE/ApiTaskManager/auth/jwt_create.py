from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from OpenSSL import rand


SECRET='ge8ZXhERUrmTic6rcHYMKKOc75qbNdiy'
ALGORITHM = 'HS256'

def expire_date(minutes: int):
    date = datetime.now()
    return date + timedelta(days=minutes)

def write_token(data: dict):
    return encode(payload={**data, "exp": expire_date(30)}, key=SECRET, algorithm=ALGORITHM)

def verify_token(token):
    try: 
        decode(token, key=SECRET, algorithms=ALGORITHM)
        return True
    except exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid Token"}, status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Token Expired"}, status_code=401)

def read_token(token):
    return decode(token, key=SECRET, algorithms=ALGORITHM)