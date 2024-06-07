from pydantic import BaseModel

class AddTaskShemaInput(BaseModel):
    user_name:str
    password:str