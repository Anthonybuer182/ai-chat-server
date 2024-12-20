from fastapi import Query, WebSocket

from src.database.postgre.model.user import UserDB
from src.http.router_auth2 import verify_token


async def get_ws_user(
    websocket: WebSocket,
    token: str = Query(None)
) -> UserDB:
    if not token:
        await websocket.close(code=1008, reason="Unauthorized")
        return
    # 验证token获取用户
    try:
        user = await verify_token(token)
        return user
    except:
        await websocket.close(code=1008, reason="Unauthorized")
        return