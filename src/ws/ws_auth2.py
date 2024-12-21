from fastapi import Query, WebSocket,status

from src.database.postgre.model.user import UserDB
from src.api.router_auth2 import verify_token


async def get_ws_user(
    websocket: WebSocket,
    token: str = Query(None)
) -> UserDB:
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Unauthorized")
        return
    # 验证token获取用户
    try:
        user = await verify_token(token)
        return user
    except:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Unauthorized")
        return