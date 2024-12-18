from fastapi import APIRouter, Depends

from src.database.postgre.connection import get_db
from src.database.postgre.model.message import get_message_list
from src.database.postgre.model.user import UserDB
from src.http.model.base import BaseResponse, success_response
from src.http.model.message import MessageListRequest
from src.http.model.pagination import PaginationResponse
from src.http.router_auth2 import get_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
@router.post("/list")
async def list(request:MessageListRequest,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    messages = await get_message_list(db,request)
    return success_response(data=messages)