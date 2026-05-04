from pydantic import BaseModel,EmailStr,Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[int] = None
    age: Optional[int] = None
    gender: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password:str

class UserResponse(BaseModel):
    id:str
    name:str
    email:str
    phone:Optional[int]=None
    age:Optional[int]=None
    gender:Optional[str]=None
    created_at:datetime