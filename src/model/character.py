from typing import Optional
from pydantic import BaseModel

from src.model.pagination import PaginationRequest


class Character(BaseModel):
    user_id:Optional[str] = None
    name: str
    background: Optional[str] = None
    portrait: Optional[str] = None
    voice: Optional[str] = None
    system_prompt: Optional[str] = None
    user_prompt: Optional[str] = None
    tts: Optional[str] = None
    visibility: Optional[str] = None
    data: Optional[dict] = None
    

class CharacterList(PaginationRequest):
    visibility: Optional[str] = None
    user_id:Optional[str] = None

