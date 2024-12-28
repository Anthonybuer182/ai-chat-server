
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from config import MAX_MESSAGE_CONTEXT_LENGTH
from src.database.postgre.model.character import get_character_by_id
from src.database.postgre.model.message import create_messages, get_message_limit
from src.database.postgre.model.session import get_session_by_id
from src.database.postgre.model.user import UserDB
from src.api.model.message import  MessageRequest
from src.api.model.user import UserRequest
from src.api.router_auth2 import  get_user
from src.api.model.base import success_response,failure_response
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.postgre.sql import get_db
from src.multi_models.llm.ai_chat import AsyncAIChat
from src.multi_models.llm.model.message import ChatMessage

router = APIRouter()

@router.post("/text")
async def text(request:MessageRequest,user:UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    session = await get_session_by_id(db,request.session_id)
    if not session:
        return failure_response(message="session not found")
    character = await get_character_by_id(db,session.character_id)
    if not character:
        return failure_response(message="character not found")
    
    # 获取向量数据库的话题上下文

    messages = await get_message_limit(db,session_id=request.session_id,limit=MAX_MESSAGE_CONTEXT_LENGTH)
    recent_messages = [ChatMessage(
            role=message.role,
            content=message.content,
            created_at=message.created_at
        ) for message in  reversed(messages)]
    ai = AsyncAIChat(model=request.model,system_prompt=request.system_prompt or character.system_prompt,messages_context=session.messages_context,recent_messages=recent_messages)
    if request.stream:
        async def generate():
            async for chunk in await ai(request.user_prompt, request.stream):
                yield chunk["token"]
        return StreamingResponse(
                generate(),
                media_type="text/plain"
            )
    else:
         text = await ai(request.user_prompt,request.stream)
    saved_messages = await create_messages(db, request, ai.new_messages)
    if not saved_messages:
        return failure_response(message="failed to save messages")
    return success_response(data=text)
@router.post("/image")
async def image(request:MessageRequest,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    return success_response(data="图像生成")
@router.get("/audio")
async def audio(request:MessageRequest,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    return success_response(data="音频生成")
@router.get("/video")
async def video(request:MessageRequest,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    return success_response(data="视频生成")

