from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: Optional[str] 
    model: str
    system_prompt: Optional[str] 
    user_prompt: Optional[str] 

