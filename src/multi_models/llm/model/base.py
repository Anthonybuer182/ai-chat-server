from abc import ABC, abstractmethod
from ast import Dict
from typing import Any, List, Optional, Union, Callable, Coroutine
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
    params:dict[str,Any] = {"temperature": 0.7}
    messages_context: Optional[str] = None # 之前的消息或者聊天话题作为上下文
    new_messages: List[ChatMessage] = []
    recent_messages: List[ChatMessage] = []
    on_word: Optional[Union[Callable[[str], None], Callable[[str], Coroutine[Any, Any, None]]]] = None
    on_sentence: Optional[Union[Callable[[str], None], Callable[[str], Coroutine[Any, Any, None]]]] = None
    current_sentence: str = ""
    class Config:
        arbitrary_types_allowed = True
    @abstractmethod
    def sync_generate_text(self, user_prompt: str, system_prompt: Optional[str]):
            pass
    @abstractmethod
    async def async_generate_text(self, user_prompt: str, system_prompt: Optional[str]):
            pass
    @abstractmethod
    def sync_generate_stream(self, user_prompt: str, system_prompt: Optional[str]):
            pass
    @abstractmethod
    async def async_generate_stream(self, user_prompt: str, system_prompt: Optional[str]):
            pass
