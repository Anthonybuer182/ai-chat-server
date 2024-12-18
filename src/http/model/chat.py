from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None, max_length=36, description="Session ID with max 36 characters")
    model: str = Field(..., description="Model name is required")
    system_prompt: Optional[str] = Field(None, description="Optional system instructions")
    user_prompt: Optional[str] = Field(None, description="Optional user instructions")
    @field_validator("model")
    def validate_non_empty(cls, value, field):
        if not value.strip():
            raise ValueError(f"{field.name.replace('_', ' ').capitalize()} cannot be empty or blank")
        return value

