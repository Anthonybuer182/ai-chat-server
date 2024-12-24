from typing import Any, Callable, Coroutine, Dict, List, Optional, Union
from uuid import UUID
from httpx import AsyncClient, Client
from pydantic import BaseModel

from src.multi_models.llm.chatgpt import ChatGPTSession
from src.multi_models.llm.model.base import ChatSession
from src.multi_models.llm.model.message import ChatMessage
from src.multi_models.llm.qwengpt import ChatQWENSession
from src.util.http import async_client, sync_client


class SyncAIChat(BaseModel):
    session: Optional[ChatSession]

    def __init__(
        self,
        model: str,
        system_prompt: Optional[str] = None,
        messages_context: Optional[str] = None,
        recent_messages: List[ChatMessage] = [],
        client: Union[Client, AsyncClient] = sync_client(),
        on_word: Optional[Union[Callable[[str], None], Callable[[str], Coroutine[Any, Any, None]]]] = None,
        on_sentence: Optional[Union[Callable[[str], None], Callable[[str], Coroutine[Any, Any, None]]]] = None
    ):
        super().__init__(session=None)
        if "gpt" in model:
            self.session = ChatGPTSession(
                client=client,
                model=model,
                system_prompt=system_prompt,
                messages_context=messages_context,
                recent_messages=recent_messages,
                on_word=on_word,
                on_sentence=on_sentence,
            )
        elif "qwen" in model:
            self.session = ChatQWENSession(
                client=client,
                model=model,
                system_prompt=system_prompt,
                messages_context=messages_context,
                recent_messages=recent_messages,
                on_word=on_word,
                on_sentence=on_sentence,
            )
        else:
            raise ValueError(f"Invalid model: {model}")

    def __call__(
        self,
        user_prompt: str,
        stream: bool = False,
        system_prompt: Optional[str] = None,
    ):
        if stream:
            return self.session.sync_generate_stream(
                user_prompt=user_prompt, system_prompt=system_prompt
            )
        else:
            return self.session.sync_generate_text(
                user_prompt=user_prompt, system_prompt=system_prompt
            )

    @property
    def new_messages(self):
        return self.session.new_messages


class AsyncAIChat(SyncAIChat):
    def __init__(
        self,
        model: str,
        system_prompt: Optional[str] = None,
        messages_context: Optional[str] = None,
        recent_messages: List[ChatMessage] = [],
        on_word: Optional[Union[Callable[[str], None], Callable[[str], Coroutine[Any, Any, None]]]] = None,
        on_sentence: Optional[Union[Callable[[str], None], Callable[[str], Coroutine[Any, Any, None]]]] = None
    ):
        super().__init__(
            model=model,
            system_prompt=system_prompt,
            messages_context=messages_context,
            recent_messages=recent_messages,
            client=async_client(),
            on_word=on_word,
            on_sentence=on_sentence
        )

    async def __call__(
        self,
        user_prompt: str,
        stream: bool = False,
        system_prompt: Optional[str] = None,
    ):
        if stream:
            return await self.session.async_generate_stream(
                user_prompt=user_prompt, system_prompt=system_prompt
            )
        else:
            return await self.session.async_generate_text(
                user_prompt=user_prompt, system_prompt=system_prompt
            )
