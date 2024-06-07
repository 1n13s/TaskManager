from pydantic import BaseModel,Field, validator
from enum import Enum, IntEnum
from typing import Optional
from datetime import date

class AddUserShemaInput(BaseModel):
    email: str = Field(min_length=1)
    user_name: str = Field(min_length=1)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    hashed_password: str = Field(min_length=1)
    is_active: bool
    class Config:
        schema_extra = {
            'example':{
                "email": "example@mail.com",
                "user_name": "jhon_doe",
                "first_name": "Jhon",
                "last_name": "Doe",
                "hashed_password": "hashed_password",
                "is_active": True
            }
        }