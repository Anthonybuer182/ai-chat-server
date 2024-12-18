from typing import Optional
from pydantic import BaseModel

from src.http.model.pagination import PaginationRequest



class CharacterRequest(BaseModel):
    id: Optional[str]
    user_id: str
    name: str
    background: Optional[str]
    portrait: Optional[str]
    voice_id: Optional[str]
    system_prompt: Optional[str]
    user_prompt: Optional[str]
    tts: Optional[str]
    visibility: Optional[bool] 
    data: Optional[dict] 
    likes: Optional[int]
    

class CharacterListRequest(PaginationRequest):
    visibility: Optional[bool] = None
    user_id:Optional[str] = None

