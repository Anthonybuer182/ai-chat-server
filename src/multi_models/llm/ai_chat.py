from typing import Dict, Optional, Union
from uuid import UUID
from httpx import AsyncClient, Client
from pydantic import BaseModel

from src.multi_models.llm.chatgpt import ChatGPTSession
from src.multi_models.llm.model.base import ChatSession
from src.multi_models.llm.qwengpt import ChatQWENSession
from src.util.http import sync_client


class AIChat(BaseModel):
    client: Union[Client,AsyncClient]
    session: Optional[ChatSession]
    def __init__(self, model: str):
        if "gpt" in model:
            self.session=ChatGPTSession(model=model,system_prompt="",messages_context="")
        elif "qwengpt" in model:
            self.session=ChatQWENSession(model=model)
        else:
                raise ValueError(f"Invalid model: {model}")
    def __call__(self,user_prompt:str,stream:bool=False):
         self.client=sync_client()