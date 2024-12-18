from pyexpat.errors import messages
from typing import Optional
from pydantic import BaseModel

from src.http.model.pagination import PaginationRequest



class SessionRequest(BaseModel):
    id: Optional[str]
    user_id : Optional[str]
    user_name : Optional[str]
    character_id: Optional[str]
    character_name: Optional[str]
    new_message : Optional[str]
    messages_context : Optional[str]

class SessionListRequest(PaginationRequest):
    user_id : Optional[str]
    character_id: Optional[str]

