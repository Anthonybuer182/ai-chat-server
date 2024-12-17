import os
from typing import Any, Optional, Set, Union, List
from fastapi import Depends
from httpx import AsyncClient, Client
import orjson
from pydantic import Field, HttpUrl
from config import DASHSCOPE_API_KEY, MAX_MESSAGE_CONTEXT_LENGTH
from src.multi_models.llm.model.base import ChatSession
from src.multi_models.llm.model.message import ChatMessage
from src.util.http import async_client, sync_client


class ChatQWENSession(ChatSession):
    api_url: HttpUrl = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    api_key: str = DASHSCOPE_API_KEY
    system_prompt: str = Field("你是一个提供帮助的助手。", exclude_none=True)
    include_fields: Set[str] = {"role", "content"}
    # def __init__(self, system_prompt: Optional[str] = None):
    #     self.system_prompt = system_prompt if system_prompt is not None else "你是一个有帮助的助手。"

    def sync_generate_text(self, user_prompt: str, system_prompt: Optional[str]):
        """Handles user interaction with the AI model."""
        headers = self._build_headers()
        messages,system_message,user_message = self._format_messages(
            system_prompt=system_prompt or self.system_prompt,
            user_prompt=user_prompt
        )
        data = self._build_request_payload(messages, False)
        
        response = self.client.post(str(self.api_url), headers=headers, json=data)
        res_json = response.json()

        assistant_message = self._parse_text_response(res_json)

        self._update_session(user_message, assistant_message)
        return assistant_message.content
    async def async_generate_text(self, user_prompt: str, system_prompt: Optional[str]):
        """Asynchronously handles user interaction with the AI model."""
        headers = self._build_headers()
        messages,system_message,user_message = self._format_messages(
            system_prompt=system_prompt or self.system_prompt,
            user_prompt=user_prompt
        )
        data = self._build_request_payload(messages, False)
       
        response = await self.client.post(str(self.api_url), headers=headers, json=data)
        res_json = response.json()

        assistant_message = self._parse_text_response(res_json)

        self._update_session(user_message, assistant_message)
        return assistant_message.content
    def sync_generate_stream(self, user_prompt: str, system_prompt: Optional[str]):
        """Handles user interaction with the AI model."""
        headers = self._build_headers()
        messages,system_message,user_message = self._format_messages(
            system_prompt=system_prompt or self.system_prompt,
            user_prompt=user_prompt
        )
        data = self._build_request_payload(messages, True)
        
        with self.client.stream(
            "POST",
            str(self.api_url),
            json=data,
            headers=headers,
        ) as response:
            content = []
            for chunk in response.iter_lines():
                delta = self._process_stream_chunk(chunk)
                if delta:
                    yield self._handle_stream_content(delta, content)

        # streaming does not currently return token counts
        assistant_message = ChatMessage(
            role="assistant",
            content=content
        )

        self._update_session(user_message, assistant_message)
        return assistant_message.content

    async def async_generate_stream(self, user_prompt: str, system_prompt: Optional[str]):
        """Handles user interaction with the AI model."""
        headers = self._build_headers()
        messages,system_message,user_message = self._format_messages(
            system_prompt=system_prompt or self.system_prompt,
            user_prompt=user_prompt
        )
        data = self._build_request_payload(messages, True)
        
        async with self.client.stream(
            "POST",
            str(self.api_url),
            json=data,
            headers=headers,
        ) as response:
            content = []
            async for chunk in response.aiter_lines():
                delta = self._process_stream_chunk(chunk)
                if delta:
                    yield self._handle_stream_content(delta, content)

        # streaming does not currently return token counts
        assistant_message = ChatMessage(
            role="assistant",
            content="".join(content),
        )

        self._update_session(user_message, assistant_message)

    def _build_headers(self) -> dict:
        """Builds and returns request headers."""
        if not self.api_key:
            raise EnvironmentError("API key is not set in the environment.")
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
    def _format_messages(self, user_prompt: str, system_prompt: Optional[str]):
        """Formats the system and user messages for the API request."""
        system_message = ChatMessage(role="system", content=system_prompt)
        user_message = ChatMessage(role="user", content=user_prompt)
        recent_messages = [
            msg.model_dump(include=self.include_fields, exclude_none=True) 
            for msg in self.recent_messages
        ]
        return [system_message.model_dump(include=self.include_fields, exclude_none=True)] + recent_messages + [
            user_message.model_dump(include=self.include_fields, exclude_none=True)
        ],system_message,user_message


    def _build_request_payload(self, messages: List[dict], stream: bool) -> dict:
        """Constructs the payload for the API request."""
        return {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            **self.params,
        }
    def _update_session(self, user_message: ChatMessage, assistant_message: ChatMessage):
        """Updates the session with new messages."""
        self.new_messages.extend([user_message, assistant_message])
        self.recent_messages.extend([user_message, assistant_message])
        if len(self.recent_messages) > MAX_MESSAGE_CONTEXT_LENGTH:
            self.recent_messages = self.recent_messages[:-2]

# text
    def _parse_text_response(self, res_json: dict) -> ChatMessage:
        """Parses the API response and creates an assistant message."""
        try:
            choice = res_json["choices"][0]["message"]
            usage = res_json.get("usage", {})
            return ChatMessage(
                role=choice["role"],
                content=choice["content"],
                finish_reason=res_json["choices"][0].get("finish_reason"),
                prompt_tokens=usage.get("prompt_tokens"),
                completion_tokens=usage.get("completion_tokens"),
                total_tokens=usage.get("total_tokens"),
            )
        except KeyError as e:
            raise ValueError(f"Unexpected response format from OpenAI API: {res_json}") from e
    # stream
    def _process_stream_chunk(self, chunk: bytes) -> Union[str, None]:
        """处理单个 SSE 数据块，移除 'data: ' 前缀并处理响应。"""
        if len(chunk) > 0:
            chunk = chunk[6:]  # 去除 "data: " 前缀
            if chunk != "[DONE]":
                chunk_dict = orjson.loads(chunk)
                delta = chunk_dict["choices"][0]["delta"].get("content")
                if delta:
                    return delta
        return None
    def _handle_stream_content(self, delta: str, content: list):
        """处理拼接后的流数据并生成响应。"""
        content.append(delta)
        return {"delta": delta, "response": ''.join(content)}