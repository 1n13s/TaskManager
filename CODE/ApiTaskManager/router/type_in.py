from pydantic import BaseModel,Field, validator
from enum import Enum, IntEnum
from typing import Optional
from datetime import date

class AddUserSchemaInput(BaseModel):
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
                "hashed_password": "password123",
                "is_active": True
            }
        }

class AddTaskSchemaInput(BaseModel):
    description: str = Field(min_length=1)
    priority: int = Field(ge=1, le=5)
    title: str = Field(min_length=1)
    complete: bool
    id_user: int

    class Config:
        schema_extra = {
            'example':{
                "description": "Complete the project documentation",
                "priority": 3,
                "title": "Documentation",
                "complete": False,
                "id_user": 1
            }
        }

class AuthUserSchemaInput(BaseModel):
    user_name: str = Field(min_length=1)
    hashed_password: str = Field(min_length=1)
    class Config:
        schema_extra = {
            'example':{
                "user_name": "jhon_doe",
                "hashed_password": "password123"
            }
        }