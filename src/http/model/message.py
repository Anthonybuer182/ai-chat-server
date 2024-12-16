from typing import Optional
from pydantic import BaseModel

from src.http.model.pagination import PaginationRequest


class MessageRequest(BaseModel):
    session_id: Optional[str] = None
    character_id: Optional[str] = None
    user_id: Optional[str] = None
    message: Optional[str] = None

class MessageListRequest(PaginationRequest):
    session_id:Optional[str] = None

