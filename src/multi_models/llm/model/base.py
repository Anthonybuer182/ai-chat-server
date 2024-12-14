from abc import ABC, abstractmethod
from ast import Dict
from typing import Any, List
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
    system_prompt: str = "You are a helpful assistant."
    old_messages_context: str # 之前的消息作为上下文
    new_messages: List[ChatMessage] = [] # 包含user和assistant 
    
    recent_messages: List[ChatMessage] = []
    recent_messages_length: int = 50
    @abstractmethod
    async def ai_chat(
        self,
        user_prompt: str,
        callback: Any,# 聊天消息的回调
    ):
        pass
# @abstractmethod
# def prepare_request(self, message: ChatMessage) -> None:
#         pass
# @abstractmethod
# def sync_text_generate(self, message: ChatMessage) -> None:
#         pass
# @abstractmethod
# def async_text_generate(self, message: ChatMessage) -> None:
#         pass
# @abstractmethod
# async def sync_text_generate(self, message: ChatMessage) -> None:
#         pass
# @abstractmethod
# def sync_stream_generate(self, message: ChatMessage) -> None:
#         pass
# @abstractmethod
# async def async_stream_generate(self, message: ChatMessage) -> None:
#         pass