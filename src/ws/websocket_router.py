from fastapi import APIRouter, Depends, HTTPException, Path, Query, WebSocket, WebSocketDisconnect
from config import MAX_MESSAGE_CONTEXT_LENGTH
from src.database.postgre.model.character import get_character_by_id
from src.database.postgre.model.message import create_messages, get_message_limit
from src.database.postgre.model.session import get_session_by_id
from src.database.postgre.model.user import UserDB
from src.http.model.message import MessageRequest
from src.multi_models.llm.model.message import ChatMessage
from src.util.logger import get_logger
from src.ws.ws_auth2 import get_ws_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.postgre.connection import get_db
from src.multi_models.llm.ai_chat import AsyncAIChat
logger = get_logger(__name__)

websocket_router = APIRouter()

@websocket_router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    token:str = Query(None),
    session_id: str = Path(...),
    model:str = Query(None),
    system_prompt: str = Query(None),
    stream:bool = Query(None),
    platform:str = Query(None),
    language:str = Query(None),
    user:UserDB = Depends(get_ws_user),
    db: AsyncSession = Depends(get_db)
    ):
    await websocket.accept()
    session = await get_session_by_id(db,session_id)
    if not session:
        await websocket.close(code=1008, reason="no session")
        return
    character = await get_character_by_id(db,session.character_id)
    if not character:
        await websocket.close(code=1008, reason="no character")
        return
    
    # 获取向量数据库的话题上下文

    messages = await get_message_limit(db,session_id=session_id,limit=MAX_MESSAGE_CONTEXT_LENGTH)
    recent_messages = [ChatMessage(
            role=message.role,
            content=message.content,
            created_at=message.created_at
        ) for message in  reversed(messages)]
    ai = AsyncAIChat(model=model,system_prompt=system_prompt or character.system_prompt,messages_context=session.messages_context,recent_messages=recent_messages)
    
    while True:
        try:
            # Receive message from client
            user_prompt = await websocket.receive_text()
            logger.info(f"Received message: {user_prompt}")
            text = await ai(user_prompt,stream)
            messageRequest = MessageRequest(session_id=session_id,model=model,system_prompt=system_prompt,stream=stream,platform=platform,language=language,user_prompt=user_prompt)
            saved_messages = await create_messages(db, messageRequest, ai.new_messages)
            await websocket.send_text(text)
        except WebSocketDisconnect:
            logger.info("Client disconnected")
            break
