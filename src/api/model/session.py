from pyexpat.errors import messages
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from src.api.model.pagination import PaginationRequest



class SessionRequest(BaseModel):
    id: Optional[str] = Field(None, max_length=36, description="Session ID with max 36")
    character_id: str = Field(..., max_length=36,description="Character ID cannot be empty and with max 36")  # 必填字段
    new_message: Optional[str] = Field(None, description="New message from the user (optional)")
    messages_context: Optional[str] = Field(None, description="Context of previous messages (optional)")
    @field_validator("character_id")
    def validate_non_empty(cls, value, field):
        if not value.strip():
            raise ValueError(f"{field.name.replace('_', ' ').capitalize()} cannot be empty or blank")
        return value

class SessionListRequest(PaginationRequest):
    character_id: Optional[str] = Field(None, max_length=36, description="Caracter ID with max 36")

