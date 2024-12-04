from fastapi import APIRouter
from src.model.character import Character, CharacterList
from src.http.base_response import BaseResponse, success_response
from src.model.pagination import PaginationResponse
router = APIRouter()
@router.post("/create")
async def create_character(request:Character,response_model=BaseResponse[Character]):
    return success_response(data=request)
@router.post("/edit")
async def create_character(request:Character,response_model=BaseResponse[Character]):
    return success_response(data=request)
@router.get("/get/{id}")
async def get_character(id: str):
    return success_response(data={id})
@router.post("/list")
async def get_characters(request:CharacterList,response_model=BaseResponse[PaginationResponse]):
    return success_response(data=PaginationResponse(page=1,page_size=10,total=0,total_pages=1,records=[request]))
