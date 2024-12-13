import os
from typing import Any
from httpx import AsyncClient, Client
from pydantic import HttpUrl
from src.multi_models.llm.model.base import ChatSession
from src.multi_models.llm.model.message import ChatMessage


class ChatGPTSession(ChatSession):
    api_url: HttpUrl = "https://api.openai.com/v1/chat/completions"
    apy_key = os.getenv("OPENAI_API_KEY")
    system_prompt = "You are a helpful assistant."

    def ai_chat(self, user_prompt: str,stream: bool = False):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.apy_key}",
        }
        system_message = ChatMessage(role="system", content=self.system_prompt)
        user_message=ChatMessage(role="user",content=user_prompt)
        messages = self.format_messages(system_message,user_message)
        data ={
            "model":self.model,
            "messages":messages,
            "stream":self.stream
            **self.params,
        }
    def format_messages(self,system_message: ChatMessage,user_message: ChatMessage):
        return (
            [system_message.model_dump(include=self.input_fields, exclude_none=True)]
            + [
                m.model_dump(include=self.input_fields, exclude_none=True)
                for m in self.recent_messages
            ]
            + [user_message.model_dump(include=self.input_fields, exclude_none=True)]
        )

