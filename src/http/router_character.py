from fastapi import APIRouter
from src.http.model.character import CharacterListRequest, CharacterRequest
from src.http.model.pagination import PaginationResponse

from src.http.model.base import BaseResponse, success_response

router = APIRouter()
@router.post("/create")
async def create_character(request:CharacterRequest):
    return success_response(data=request)
@router.post("/edit")
async def create_character(request:CharacterRequest):
    return success_response(data=request)
@router.get("/get/{id}")
async def get_character(id: str):
    return success_response(data={id})
@router.post("/list")
async def get_characters(request:CharacterListRequest):
    return success_response(data=PaginationResponse(page=1,page_size=10,total=0,total_pages=1,records=[request]))
