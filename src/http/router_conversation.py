from fastapi import APIRouter
from src.http.model.base import success_response
from src.http.model.conversation import ConversationListRequest
from src.http.model.pagination import PaginationResponse

router = APIRouter()

@router.post("/list")
async def get_conversations(request:ConversationListRequest):
    return success_response(data=PaginationResponse(page=1,page_size=10,total=0,total_pages=1,records=[request]))
