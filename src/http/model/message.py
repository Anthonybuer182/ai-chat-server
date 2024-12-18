from typing import Optional
from pydantic import BaseModel, Field, field_validator

from src.http.model.pagination import PaginationRequest


class MessageRequest(BaseModel):
    id: Optional[str] = Field(None, max_length=36, description="Session ID with max 36")
    session_id: str = Field(..., max_length=36,description="Session ID cannot be empty")  # 必填字段
    platform: str = Field(..., description="Platform cannot be empty")  # 必填字段
    language: str = Field(..., description="Language cannot be empty")  # 必填字段
    model: str = Field(..., description="Model name cannot be empty")  # 必填字段
    request_id: Optional[str] = Field(None, description="Request ID (optional)")
    role: str = Field(..., description="Role cannot be empty")  # 必填字段
    content: str = Field(..., description="Content cannot be empty")  # 必填字段
    finish_reason: Optional[str] = Field(None, description="Reason for message completion (optional)")
    prompt_tokens: Optional[int] = Field(None, ge=0, description="Number of tokens in the prompt (optional, non-negative)")
    completion_tokens: Optional[int] = Field(None, ge=0, description="Number of tokens in the completion (optional, non-negative)")
    total_tokens: Optional[int] = Field(None, ge=0, description="Total tokens used (optional, non-negative)")

    @field_validator("session_id", "platform", "language", "model", "role", "content")
    def validate_non_empty(cls, value, field):
        if not value.strip():  
            raise ValueError(f"{field.name.replace('_', ' ').capitalize()} cannot be empty or blank")
        return value

class MessageListRequest(PaginationRequest):
    session_id:Optional[str]= Field(None, max_length=36, description="Session ID with max 36")

