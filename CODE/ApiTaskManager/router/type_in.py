from pydantic import BaseModel,Field
from enum import Enum, IntEnum
from typing import Optional
from datetime import date

class AddUserSchemaInput(BaseModel):
    email: str = Field(min_length=1)
    user_name: str = Field(min_length=1)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    hashed_password: str = Field(min_length=1)
    is_admin: bool
    class Config:
        schema_extra = {
            'example':{
                "email": "example@mail.com",
                "user_name": "jhon_doe",
                "first_name": "Jhon",
                "last_name": "Doe",
                "hashed_password": "password123",
                "is_admin": True
            }
        }

class AddTaskSchemaInput(BaseModel):
    description: str = Field(min_length=1)
    priority: int = Field(ge=1, le=5)
    title: str = Field(min_length=1)
    complete: bool

    class Config:
        schema_extra = {
            'example':{
                "description": "Complete the project documentation",
                "priority": 3,
                "title": "Documentation",
                "complete": False
            }
        }

class UpdateTaskShemaInput(AddTaskSchemaInput):
    id: int
    class Config:
        schema_extra = {
            'example':{
                "id": 1,
                "description": "Complete the project documentation",
                "priority": 3,
                "title": "Documentation",
                "complete": False
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

class UseTaskIdSchemaInput(BaseModel):
    id_task: int = Field(ge=1)
    class Config:
        schema_extra = {
            'example':{
                "id_task": 2
            }
        }

class UpdateTaskStateInput(UseTaskIdSchemaInput):
    complete: bool
    class Config:
        schema_extra = {
            'example':{
                "id_task": 1,
                "complete": True
            }
        }

class ChangeUserPassword(BaseModel):
    current_password: str
    new_password: str

    class Config:
        schema_extra = {
            'example':{
                "current_password": "currentpassword",
                "new_password": "newpassword"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str