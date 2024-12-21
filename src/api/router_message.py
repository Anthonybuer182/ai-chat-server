from fastapi import APIRouter, Depends

from src.database.postgre.connection import get_db
from src.database.postgre.model.message import get_message_list
from src.database.postgre.model.user import UserDB
from src.api.model.base import BaseResponse, success_response
from src.api.model.message import MessageListRequest
from src.api.model.pagination import PaginationResponse
from src.api.router_auth2 import get_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
@router.post("/list")
async def list(request:MessageListRequest,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    messages = await get_message_list(db,request)
    return success_response(data=messages)