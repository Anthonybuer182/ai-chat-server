from fastapi import APIRouter

from src.http.model.base import BaseResponse, success_response
from src.http.model.chat import ChatRequest

router = APIRouter()

@router.post("/text")
async def text(request:ChatRequest,response_model=BaseResponse[str]):
    return success_response(data="输出")

