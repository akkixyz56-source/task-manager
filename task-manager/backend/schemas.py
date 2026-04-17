from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str
    
class ProjectCreate(BaseModel):
    project_name: str
    description: str

class ProjectUpdate(BaseModel):
    project_name: str
    description: str

class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime

class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str
    due_date: datetime
    
    
class AssignTask(BaseModel):
    user_id: int

