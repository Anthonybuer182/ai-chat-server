import os
from typing import Any, Set, Union
from fastapi import Depends
from httpx import AsyncClient, Client
from pydantic import HttpUrl
from src.multi_models.llm.model.base import ChatSession
from src.multi_models.llm.model.message import ChatMessage


class ChatGPTSession(ChatSession):
    api_url: HttpUrl = "https://api.openai.com/v1/chat/completions"
    apy_key = os.getenv("OPENAI_API_KEY")
    system_prompt = "You are a helpful assistant."
    include_fields: Set[str] = {"role", "content"}

    def prepare_request(self, user_prompt: str,stream: bool = False):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
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
        return headers,messages
        

    def format_messages(self,system_message: ChatMessage,user_message: ChatMessage):
        return (
            [system_message.model_dump(include=self.include_fields, exclude_none=True)]
            + [
                m.model_dump(include=self.include_fields, exclude_none=True)
                for m in self.recent_messages
            ]
            + [user_message.model_dump(include=self.include_fields, exclude_none=True)]
        )

    def sync_text_generate(self, client: Union[Client, AsyncClient], headers:dict[str,str], data:list[dict[str,Any]]):
        response = client.post(str(self.api_url),headers=headers,json=data)
        res_json=response.json()
        try:
            res_content=res_json["choices"][0]["message"]["content"]
            assistant_message = ChatMessage(
            role=res_json["choices"][0]["message"]["role"],
            content=res_content,
            finish_reason=res_json["choices"][0]["finish_reason"],
            prompt_tokens=res_json["usage"]["prompt_tokens"],
            completion_tokens=res_json["usage"]["completion_tokens"],
            total_tokens=res_json["usage"]["total_tokens"],
        )
        except KeyError:
            raise ValueError(f"Unexpected response from OpenAI API: {res_json}")
        return res_content
    def async_text_generate(self, message: ChatMessage) -> None:
        pass
