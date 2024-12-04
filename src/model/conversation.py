from typing import Optional
from pydantic import BaseModel

from src.model.pagination import PaginationRequest


class Conversation(BaseModel):
    user_id: Optional[str] = None
    character_id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None

class ConversationList(PaginationRequest):
    user_id: Optional[str] = None
    character_id: Optional[str] = None

