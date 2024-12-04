from fastapi import APIRouter

from src.http.base_response import BaseResponse, success_response
from src.model.message import MessageList
from src.model.pagination import PaginationResponse
router = APIRouter()
@router.post("/list")
async def get_chats(request:MessageList,response_model=BaseResponse[PaginationResponse]):
    return success_response(data=PaginationResponse(page=1,page_size=10,total=0,total_pages=1,records=[request]))
