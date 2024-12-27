from fastapi import Query, WebSocket,status

from src.database.postgre.model.user import UserDB
from src.api.router_auth2 import verify_token


async def get_ws_user(
    token: str = Query(None)
) -> UserDB:
    if not token:
        return
    # 验证token获取用户
    try:
        user = verify_token(token)
        return user
    except Exception as e:
        return