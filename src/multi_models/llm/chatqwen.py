import os
from typing import Any, Set, Union, List
from fastapi import Depends
from httpx import AsyncClient, Client
import orjson
from pydantic import HttpUrl
from src.multi_models.llm.model.base import ChatSession
from src.multi_models.llm.model.message import ChatMessage
from src.util.http import async_client, sync_client


class ChatGPTSession(ChatSession):
    api_url: HttpUrl = "https://api.openai.com/v1/chat/completions"
    api_key = os.getenv("OPENAI_API_KEY")
    system_prompt = "You are a helpful assistant."
    include_fields: Set[str] = {"role", "content"}

    def sync_generate_text(self, system_prompt: str, user_prompt: str):
        """Handles user interaction with the AI model."""
        headers = self._build_headers()
        messages,system_message,user_message = self.format_messages(
            system_prompt=system_prompt or self.system_prompt,
            user_prompt=user_prompt
        )
        data = self._build_request_payload(messages, False)
        
        response = sync_client().post(str(self.api_url), headers=headers, json=data)
        res_json = response.json()

        assistant_message = self._parse_text_response(res_json)

        self._update_session(user_message, assistant_message)
        return assistant_message.content
    async def async_generate_text(self, system_prompt: str, user_prompt: str):
        """Asynchronously handles user interaction with the AI model."""
        headers = self._build_headers()
        messages,system_message,user_message = self.format_messages(
            system_prompt=system_prompt or self.system_prompt,
            user_prompt=user_prompt
        )
        data = self._build_request_payload(messages, False)
       
        response = await async_client().post(str(self.api_url), headers=headers, json=data)
        res_json = response.json()

        assistant_message = self._parse_text_response(res_json)

        self._update_session(user_message, assistant_message)
        return assistant_message.content
    def sync_generate_stream(self, system_prompt: str, user_prompt: str):
        """Handles user interaction with the AI model."""
        headers = self._build_headers()
        messages,system_message,user_message = self.format_messages(
            system_prompt=system_prompt or self.system_prompt,
            user_prompt=user_prompt
        )
        data = self._build_request_payload(messages, True)
        
        with sync_client().stream(
            "POST",
            str(self.api_url),
            json=data,
            headers=headers,
            timeout=None,
        ) as response:
            content = []
            for chunk in response.iter_lines():
                if len(chunk) > 0:
                    chunk = chunk[6:]  # SSE JSON chunks are prepended with "data: "
                    if chunk != "[DONE]":
                        chunk_dict = orjson.loads(chunk)
                        delta = chunk_dict["choices"][0]["delta"].get("content")
                        if delta:
                            content.append(delta)
                            yield {"delta": delta, "response": "".join(content)}

        # streaming does not currently return token counts
        assistant_message = ChatMessage(
            role="assistant",
            content="".join(content),
        )

        self._update_session(user_message, assistant_message)
        return assistant_message.content

    def async_generate_stream(self, system_prompt: str, user_prompt: str):
        """Handles user interaction with the AI model."""
        headers = self._build_headers()
        messages,system_message,user_message = self.format_messages(
            system_prompt=system_prompt or self.system_prompt,
            user_prompt=user_prompt
        )
        data = self._build_request_payload(messages, True)
        
        with async_client().stream(
            "POST",
            str(self.api_url),
            json=data,
            headers=headers,
            timeout=None,
        ) as response:
            content = []
            for chunk in response.iter_lines():
                if len(chunk) > 0:
                    chunk = chunk[6:]  # SSE JSON chunks are prepended with "data: "
                    if chunk != "[DONE]":
                        chunk_dict = orjson.loads(chunk)
                        delta = chunk_dict["choices"][0]["delta"].get("content")
                        if delta:
                            content.append(delta)
                            yield {"delta": delta, "response": "".join(content)}

        # streaming does not currently return token counts
        assistant_message = ChatMessage(
            role="assistant",
            content="".join(content),
        )

        self._update_session(user_message, assistant_message)
        return assistant_message.content

    def _build_headers(self) -> dict:
        """Builds and returns request headers."""
        if not self.api_key:
            raise EnvironmentError("API key is not set in the environment.")
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
    def format_messages(self, system_prompt: str, user_prompt: str):
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

        # Limit to most recent two messages for session context
        self.recent_messages = [
            msg for msg in self.recent_messages[-2:]
            if msg.role == "assistant" or len(self.recent_messages) <= 2
        ]
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
        except KeyError:
            raise ValueError(f"Unexpected response from OpenAI API: {res_json}")