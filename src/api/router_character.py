from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from src.api.model.pagination import PaginationRequest
from src.database.postgre._sql import get_db
from src.database.postgre.character_sql import create_character, delete_character, edit_character, get_character_by_id, get_character_list
from src.database.postgre.model.user import UserDB
from src.api.model.character import CharacterListRequest, CharacterRequest
from src.api.model.base import  failure_response, success_response
from src.api.router_auth2 import get_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
@router.post("/create")
async def create(request:CharacterRequest,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    character=await create_character(db, user_id=user.id, character=request)
    return success_response(data=jsonable_encoder(character))

@router.post("/delete/{id}")
async def delete(id:str,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    result=await delete_character(db, user_id=user.id, character_id=id)
    return success_response(data=result)

@router.post("/edit")
async def edit(request:CharacterRequest,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    character=await edit_character(db,user_id=user.id,character=request)
    if not character:
        return failure_response(message="character not found")
    return success_response(data=jsonable_encoder(character))

@router.get("/get/{id}")
async def get(id: str,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    character=await get_character_by_id(db,id)
    return success_response(data=jsonable_encoder(character))

@router.post("/list")
async def list(request:CharacterListRequest,db: AsyncSession = Depends(get_db)):
    characters=await get_character_list(db,characterList=request)
    return success_response(data=characters)
@router.post("/my")
async def list(request:PaginationRequest,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    characters=await get_character_list(db,user_id=user.id,characterList=request)
    return success_response(data=characters)
