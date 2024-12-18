import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    request_id: Optional[str] = None
    role: str
    content: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    finish_reason: Optional[str] = None
    prompt_tokens:  Optional[int] = None
    completion_tokens:  Optional[int] = None
    total_tokens:  Optional[int] = None