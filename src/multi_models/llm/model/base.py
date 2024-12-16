from abc import ABC, abstractmethod
from ast import Dict
from typing import Any, List, Optional, Union
from uuid import UUID, uuid4
from httpx import AsyncClient, Client
from pydantic import BaseModel, Field

from src.multi_models.llm.model.message import ChatMessage


class ChatSession(BaseModel,ABC):
    client: Union[Client, AsyncClient]
    id: Union[str, UUID] = Field(default_factory=uuid4)
    api_url: str
    api_key: str
    model: str
    params:Dict[str,Any] = {"temperature": 0.7}
    messages_context: Optional[str] # 之前的消息或者聊天话题作为上下文
    new_messages: List[ChatMessage] = []
    recent_messages: List[ChatMessage] = []

    @abstractmethod
    def sync_generate_text(self, system_prompt: Optional[str], user_prompt: str):
            pass
    @abstractmethod
    def async_generate_text(self, system_prompt: Optional[str], user_prompt: str):
            pass
    @abstractmethod
    def sync_generate_stream(self, system_prompt: Optional[str], user_prompt: str):
            pass
    @abstractmethod
    def async_generate_stream(self, system_prompt: Optional[str], user_prompt: str):
            pass
