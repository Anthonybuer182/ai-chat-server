import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    request_id:str
    role: str
    content: str
    finish_reason: Optional[str] = None
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int