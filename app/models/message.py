from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class MessageCreate(BaseModel):#this function is used to create the message schema for the request body while sending the message from the user to the assistant
    content: str
    session_id:str

class MessageInDB(BaseModel):#this function is used to create the message schema for the database and it will be used in the api files to perform database operations
    user_id: str
    session_id:str

    role: Literal["user","assistant"]
    content: str
    timestamp: datetime
    is_emergency: bool = False

class conversationSummary(BaseModel):#thsi function is used to create the conversation summary schema for the database and it will be used in the api files to perform database operations
    session_id: str
    user_id: str
    summary: str
    message_count: int
    created_at: datetime
    updated_at: datetime
