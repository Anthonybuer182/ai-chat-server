from typing import Optional
from pydantic import BaseModel, Field, field_validator

from src.http.model.pagination import PaginationRequest


class MessageRequest(BaseModel):
    id: Optional[str] = Field(None, max_length=36, description="Session ID with max 36")
    session_id: str = Field(..., max_length=36,description="Session ID cannot be empty")
    model: str = Field(..., description="Model name cannot be empty")
    system_prompt: Optional[str] = Field(None, description="Optional system instructions")
    user_prompt: str = Field(..., description="User prompt cannot be empty")
    stream:Optional[bool] = Field(None, description = "Optional stream status")
    platform: str = Field(..., description="Platform cannot be empty") 
    language: str = Field(..., description="Language cannot be empty")

    @field_validator("session_id", "model", "platform", "language")
    def validate_non_empty(cls, value, field):
        if not value.strip():  
            raise ValueError(f"{field.name.replace('_', ' ').capitalize()} cannot be empty or blank")
        return value

class MessageListRequest(PaginationRequest):
    session_id:Optional[str]= Field(None, max_length=36, description="Session ID with max 36")

