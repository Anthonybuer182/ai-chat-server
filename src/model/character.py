from typing import Optional
from pydantic import BaseModel

from src.model.pagination import PaginationRequest


class Character(BaseModel):
    name: str
    background: Optional[str] = None
    portrait: Optional[str] = None
    voice: Optional[str] = None
    system_prompt: Optional[str] = None
    user_prompt: Optional[str] = None
    tts: Optional[str] = None
    visibility: Optional[str] = None
    data: Optional[dict] = None
    create_by:Optional[str] = None

class CharacterList(PaginationRequest):
    visibility: Optional[str] = None
    create_by:Optional[str] = None

