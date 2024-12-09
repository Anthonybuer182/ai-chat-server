from typing import Optional
from pydantic import BaseModel

from src.http.model.pagination import PaginationRequest



class ConversationRequest(BaseModel):
    user_id: Optional[str] = None
    character_id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None

class ConversationListRequest(PaginationRequest):
    user_id: Optional[str] = None
    character_id: Optional[str] = None

