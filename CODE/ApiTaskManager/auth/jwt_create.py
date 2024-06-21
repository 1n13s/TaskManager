from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from typing import Dict
from ..core.user_manager import UserManager
from OpenSSL import rand


SECRET='ge8ZXhERUrmTic6rcHYMKKOc75qbNdiy'
ALGORITHM = 'HS256'
