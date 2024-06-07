from pydantic import BaseModel,Field, validator
from enum import Enum, IntEnum
from typing import Optional
from datetime import date

class AddUserShemaInput(BaseModel):
    user_name: str = Field(min_length=1)
    password: str = Field(min_length=1)
    class Config:
        schema_extra = {
            'example':{
                "user_name": "ivonne_125",
                "password": "pass123"
            }
        }