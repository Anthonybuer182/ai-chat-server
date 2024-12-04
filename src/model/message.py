from typing import Optional
from pydantic import BaseModel

from src.model import conversation
from src.model.pagination import PaginationRequest

class Message(BaseModel):
    conversation_id: Optional[str] = None
    character_id: Optional[str] = None
    user_id: Optional[str] = None
    message: Optional[str] = None

class MessageList(PaginationRequest):
    conversation_id:Optional[str] = None

