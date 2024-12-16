from typing import Optional
from pydantic import BaseModel

from src.http.model.pagination import PaginationRequest



class SessionRequest(BaseModel):
    user_id: Optional[str] = None
    character_id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None

class SessionListRequest(PaginationRequest):
    user_id: Optional[str] = None
    character_id: Optional[str] = None

