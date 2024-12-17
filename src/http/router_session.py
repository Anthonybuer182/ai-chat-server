from fastapi import APIRouter, Depends
from src.database.postgre.connection import get_db
from src.http.model.base import success_response
from src.http.model.session import SessionListRequest
from src.http.model.pagination import PaginationResponse
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()

@router.post("/list")
async def get_sessions(request:SessionListRequest,db: AsyncSession = Depends(get_db)):
    
    return success_response(data=PaginationResponse(page=1,page_size=10,total=0,total_pages=1,records=[request]))
