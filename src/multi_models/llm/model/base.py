from abc import ABC, abstractmethod
from ast import Dict
from typing import Any, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel

from src.multi_models.llm.model.message import ChatMessage


class ChatSession(BaseModel,ABC):
    conversation_id: str
    conversation_name: str
    api_url: str
    api_key: str
    model: str
    params:Dict[str,Any] = {"temperature": 0.7}
    system_prompt: Optional[str] = "You are a helpful assistant."
    old_messages_context: Optional[str] # 之前的消息作为上下文
    new_messages: List[ChatMessage] = [] # 包含user和assistant 
    
    recent_messages: List[ChatMessage] = []
    recent_messages_length: int = 50

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
