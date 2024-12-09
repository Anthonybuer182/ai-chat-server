from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: Optional[str] = None
    character_id: Optional[str] = None
    conversation_id: Optional[str] = None
    message: Optional[str] = None
    model: Optional[str] = None
    api_key: Optional[str] = None
    temperature: Optional[str] = None
    stream: Optional[bool] = None

