from typing import Dict, Optional
from pydantic import BaseModel, Field, field_validator
from src.api.model.pagination import PaginationRequest

class CharacterRequest(BaseModel):
    id: Optional[str] = Field(None, max_length=36, description="Character ID (optional)")
    name: str = Field(..., description="Character name cannot be empty")  # 必填字段
    background: str = Field(..., description="Character background or story (optional)")
    portrait: Optional[str] = Field(None, description="URL of the character portrait (optional)")
    voice_id: Optional[str] = Field(None, description="Voice ID for TTS (optional)")
    system_prompt: Optional[str] = Field(None, description="System prompt text (optional)")
    tts: Optional[str] = Field(None, description="Text-to-speech configuration (optional)")
    visibility: bool = Field(..., description="Visibility status cannot be empty")  # 必填字段
    data: Optional[Dict] = Field(None, description="Additional character data (optional)")
    likes: Optional[int] = Field(None, ge=0, description="Number of likes (optional, non-negative)")

    @field_validator("name")
    def validate_non_empty(cls, value, field):
        if not value.strip():
            raise ValueError(f"{field.name.capitalize()} cannot be empty or blank")
        return value
    

class CharacterListRequest(PaginationRequest):
    visibility: Optional[bool] = Field(None, description="Visibility status; can be True, False, or None if not specified")
    user_id: Optional[str] = Field(None, max_length=36, description="User ID with max 36")

