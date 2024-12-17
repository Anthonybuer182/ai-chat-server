from math import ceil
import uuid
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import JSON, Boolean, Column, Enum, ForeignKey, Integer,String, Text, func

from src.database.postgre.model.base import BaseDB
from src.http.model.character import CharacterListRequest, CharacterRequest
from src.http.model.pagination import PaginationResponse
class SessionDB(BaseDB):
    __tablename__ = "sessions"
    id = Column(String(36), primary_key=True, index=True, nullable=False, doc="会话唯一标识符。")
    user_id = Column(String(36), ForeignKey("users.id"), index=True, nullable=False, doc="关联的用户ID")
    character_id = Column(String(36), ForeignKey("characters.id"), index=True, nullable=False, doc="角色ID")
    character_name = Column(String(128), index=True, nullable=False, doc="角色名称")
    character_portrait = Column(String(256), index=True, nullable=False, doc="角色头像")
    new_message = Column(Text, index=True, nullable=False, doc="最新消息")
    messages_context = Column(Text,nullable=False, doc="历史消息上下文")
    
    
  

async def create_char(db: AsyncSession,user_id: str, character: CharacterRequest):
    db_character = SessionDB(id=str(uuid.uuid4().hex),user_id=user_id,**character.model_dump(exclude={"id"}))
    db.add(db_character)
    await db.commit()
    await db.refresh(db_character)
    return db_character
async def edit_char(db: AsyncSession, user_id: str, character: CharacterRequest):
    async with db.begin():
        result = await db.execute(select(SessionDB).filter(SessionDB.id == character.id, SessionDB.user_id == user_id))
        db_character = result.scalars().first()

        if not db_character:
            return None  
        character_data = character.model_dump(exclude={"id", "user_id"})
        for key, value in character_data.items():
            if hasattr(db_character, key) and value is not None and value != "":
                setattr(db_character, key, value)
        await db.commit()
        return db_character
async def get_char_by_name(db: AsyncSession, character_name: str):
    async with db.begin():
        result = await db.execute(select(SessionDB).filter(SessionDB.name == character_name))
        return result.scalars().first()
    
async def get_char_by_id(db: AsyncSession, character_id: str):
    async with db.begin():
        result = await db.execute(select(SessionDB).filter(SessionDB.id == character_id))
        return result.scalars().first()

async def get_char_list(db: AsyncSession, characterList: CharacterListRequest) -> PaginationResponse[dict]:
    base_query = select(SessionDB)

    if characterList.visibility is not None:
        base_query = base_query.filter(SessionDB.visibility == characterList.visibility)
    if characterList.user_id:
        base_query = base_query.filter(SessionDB.user_id == characterList.user_id)

    count_query = base_query.with_only_columns(func.count()).order_by(None)
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    offset = (characterList.page - 1) * characterList.page_size
    paginated_query = base_query.offset(offset).limit(characterList.page_size)

    result = await db.execute(paginated_query)
    records = result.scalars().all()

    total_pages = ceil(total / characterList.page_size) if total > 0 else 0

    response_records = [record.__dict__ for record in records]
    
    for record in response_records:
        record.pop('_sa_instance_state', None)

    return PaginationResponse[dict](
        total=total,
        total_pages=total_pages,
        page=characterList.page,
        page_size=characterList.page_size,
        records=response_records,
    )

