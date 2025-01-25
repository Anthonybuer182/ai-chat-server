from typing import Optional
from pydantic import BaseModel, Field, field_validator

from src.api.model.pagination import PaginationRequest


class MessageRequest(BaseModel):
    id: Optional[str] = Field(None, max_length=36, description="Message ID with max 36")
    character_id: str = Field(..., max_length=36,description="Character ID cannot be empty")
    model: str = Field(..., description="Model name cannot be empty")
    system_prompt: Optional[str] = Field(None, description="Optional system instructions")
    user_prompt: str = Field(..., description="User prompt cannot be empty")
    stream:Optional[bool] = Field(None, description = "Optional stream status")
    platform: str = Field(..., description="Platform cannot be empty") 
    language: str = Field(..., description="Language cannot be empty")

    @field_validator("character_id", "model", "platform", "language")
    def validate_non_empty(cls, value, field):
        if not value.strip():  
            raise ValueError(f"{field.name.replace('_', ' ').capitalize()} cannot be empty or blank")
        return value

class MessageListRequest(PaginationRequest):
    character_id:Optional[str]= Field(None, max_length=36, description="Character ID with max 36")

