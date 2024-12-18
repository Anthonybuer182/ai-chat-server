from typing import Optional
from pydantic import BaseModel

from src.http.model.pagination import PaginationRequest


class MessageRequest(BaseModel):
    id: Optional[str] 
    session_id: Optional[str] 
    platform: Optional[str]
    language: Optional[str]
    model : Optional[str]
    request_id: Optional[str]
    role: Optional[str]
    content: Optional[str]
    finish_reason: Optional[str]
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]

class MessageListRequest(PaginationRequest):
    session_id:Optional[str]

