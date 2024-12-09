from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from src.database.postgre.connection import get_db
from src.database.postgre.model.character import create_char, edit_char, get_char_by_id
from src.database.postgre.model.user import UserDB
from src.http.model.character import CharacterListRequest, CharacterRequest
from src.http.model.pagination import PaginationResponse

from src.http.model.base import  failure_response, success_response
from src.http.router_auth2 import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
@router.post("/create")
async def create_character(request:CharacterRequest,current_user: UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    character=await create_char(db,user_id=current_user.id,character=request)
    return success_response(data=jsonable_encoder(character))
@router.post("/edit")
async def edit_character(request:CharacterRequest,current_user: UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    character=await edit_char(db,user_id=current_user.id,character=request)
    if not character:
        return failure_response(message="character not found")
    return success_response(data=jsonable_encoder(character))
@router.get("/get/{id}")
async def get_character(id: str,current_user: UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    character=await get_char_by_id(db,id)
    return success_response(data=jsonable_encoder(character))
@router.post("/list")
async def get_characters(request:CharacterListRequest,current_user: UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return success_response(data=PaginationResponse(page=1,page_size=10,total=0,total_pages=1,records=[request]))
