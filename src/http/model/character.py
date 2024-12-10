from typing import Optional
from pydantic import BaseModel

from src.http.model.pagination import PaginationRequest



class CharacterRequest(BaseModel):
    id: Optional[str]
    name: str
    background: Optional[str] = None
    portrait: Optional[str] = None
    voice_id: Optional[str] = None
    system_prompt: Optional[str] = None
    user_prompt: Optional[str] = None
    tts: Optional[str] = None
    visibility: Optional[bool] = None
    data: Optional[dict] = None
    

class CharacterListRequest(PaginationRequest):
    visibility: Optional[bool] = None
    user_id:Optional[str] = None

