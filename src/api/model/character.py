from pydoc_data import topics
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator
from src.api.model.pagination import PaginationRequest

class CharacterRequest(BaseModel):
    id: Optional[str] = None
    name: str
    sex: Optional[str] = None
    age: Optional[int] = None
    job: Optional[str] = None
    hobby: Optional[str] = None
    system_prompt: Optional[str]= None
    voice: Optional[str] = None
    style: Optional[str] = None
    avatars: Optional[List[str]] = None
    topics: Optional[List[str]] = None
    likes: Optional[int] = None
    visibility: Optional[bool] = True
    # background: Optional[str] = Field(None, description="Character background or story (optional)")
    tts: Optional[str] = None
    data: Optional[Dict] = None


    @field_validator("name")
    def validate_non_empty(cls, value, field):
        if not value.strip():
            raise ValueError(f"{field.name.capitalize()} cannot be empty or blank")
        return value
    

class CharacterListRequest(PaginationRequest):
    visibility: Optional[bool] = Field(None, description="Visibility status; can be True, False, or None if not specified")

