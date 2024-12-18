from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from src.database.postgre.connection import get_db
from src.database.postgre.model.character import create_character, edit_character, get_character_by_id, get_character_list
from src.database.postgre.model.user import UserDB
from src.http.model.character import CharacterListRequest, CharacterRequest
from src.http.model.pagination import PaginationResponse

from src.http.model.base import  failure_response, success_response
from src.http.router_auth2 import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
@router.post("/create")
async def create(request:CharacterRequest,current_user: UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    character=await create_character(db, character=request, user_id=current_user.id)
    return success_response(data=jsonable_encoder(character))
@router.post("/edit")
async def edit(request:CharacterRequest,current_user: UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    character=await edit_character(db,character=request, user_id=current_user.id)
    if not character:
        return failure_response(message="character not found")
    return success_response(data=jsonable_encoder(character))
@router.get("/get/{id}")
async def get(id: str,current_user: UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    character=await get_character_by_id(db,id)
    return success_response(data=jsonable_encoder(character))
@router.post("/list")
async def list(request:CharacterListRequest,current_user: UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    characterList=await get_character_list(db,characterList=request)
    return success_response(data=characterList)
