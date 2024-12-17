from typing import Optional
from pydantic import BaseModel

from src.http.model.pagination import PaginationRequest



class SessionRequest(BaseModel):
    character_id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None

class SessionListRequest(PaginationRequest):
    character_id: Optional[str] = None

