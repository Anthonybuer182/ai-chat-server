import re
from fastapi import APIRouter, Depends, Path, Query, WebSocket, WebSocketDisconnect, status
from config import MAX_MESSAGE_CONTEXT_LENGTH
from src.database.postgre.character_sql import get_character_by_id
from src.database.postgre.message_sql import create_messages, get_message_limit
from src.database.postgre.session_sql import get_session_by_id
from src.database.postgre.model.user import UserDB
from src.api.model.message import MessageRequest
from src.multi_models.llm.model.message import ChatMessage
from src.util.logger import get_logger
from src.ws.connection_manager import ConnectionManager
from src.ws.ws_auth2 import get_ws_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.postgre._sql import get_db
from src.multi_models.llm.ai_chat import AsyncAIChat

logger = get_logger(__name__)

websocket_router = APIRouter()
manager = ConnectionManager()

@websocket_router.websocket("/ws/{character_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(None),
    character_id: str = Path(...),
    model: str = Query(None),
    system_prompt: str = Query(None),
    stream: bool = Query(None),
    platform: str = Query(None),
    language: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    # 获取用户信息
    user = await get_ws_user(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="token is none or invalid")
        return

    # 连接到 WebSocket
    await manager.connect(websocket, user.id, character_id)
    try:
        # 会话验证
        session = await get_session_by_id(db, user_id=user.id, character_id=character_id)
        if not session:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="no session")
            return

        # 获取角色信息
        character = await get_character_by_id(db, character_id)
        if not character:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="no character")
            return

        # 获取消息上下文
        messages = await get_message_limit(db, user_id=user.id, character_id=character_id, limit=MAX_MESSAGE_CONTEXT_LENGTH)
        recent_messages = [
            ChatMessage(
                role=message.role,
                content=message.content,
                created_at=message.created_at
            ) for message in reversed(messages)
        ]

        # 初始化 AI 聊天实例
        ai = AsyncAIChat(
            model=model,
            system_prompt=system_prompt or character.system_prompt,
            messages_context=session.messages_context,
            recent_messages=recent_messages,
        )

        # 处理 WebSocket 消息
        while True:
            try:
                # 接收用户消息
                user_prompt = await websocket.receive_text()
                logger.info(f"Received message from user {user.id} and character {character_id}: {user_prompt}")

                # 生成 AI 回应
                sentence = ""
                async for chunk in await ai(user_prompt, stream):
                    token = chunk["token"]
                    for char in token:
                        if re.match(r"[,.\?!，。？！\n\r\t]", char):
                            sentence += char
                            if sentence.strip():
                                # 将消息放入队列，广播给用户和角色
                                await manager.message_queue.put(({"message": sentence}, user.id, character_id))
                                sentence = ""
                        else:
                            sentence += char

                # 保存消息到数据库
                message_request = MessageRequest(
                    character_id=character_id,
                    model=model,
                    system_prompt=system_prompt,
                    stream=stream,
                    platform=platform,
                    language=language,
                    user_prompt=user_prompt
                )
                saved_messages = await create_messages(db, user.id, message_request, ai.new_messages)

            except WebSocketDisconnect:
                logger.info(f"Client disconnected for user {user.id} and character {character_id}")
                break

            except Exception as e:
                logger.error(f"Error in WebSocket endpoint for user {user.id} and character {character_id}: {e}")
                break

    finally:
        # 断开连接
        await manager.disconnect(websocket, user.id, character_id)