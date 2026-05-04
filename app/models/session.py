from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionCreate(BaseModel):#
    user_id: str

class SessionInDB(BaseModel):#this function is used to create the session schema for the database and it will be used in the api files to perform database operations
    user_id: str
    session_id:str
    started_at: datetime
    ended_at:Optional[datetime] = None
    summary:Optional[str] = None
    key_symptoms:list[str] = []
    message_count:int = 0
    is_active: bool = True

class SessionResponse(BaseModel):#this function is used to create the session response schema for the response body while creating the session and it will be used in the api files to return the response after creating the session
    session_id: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    summary:Optional[str] = None
    key_symptoms: list[str] = []
    message_count:int 