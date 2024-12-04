from fastapi import APIRouter

from src.http.base_response import BaseResponse, success_response
from src.model.chat import  Chat
router = APIRouter()

@router.post("/text")
async def text(request:Chat,response_model=BaseResponse[str]):
    return success_response(data="输出")

