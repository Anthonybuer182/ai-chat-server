from math import ceil
import uuid
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer,String, func
from sqlalchemy.dialects.postgresql import UUID, ENUM
from src.database.postgre.model.base import BaseDB
from src.api.model.character import CharacterListRequest, CharacterRequest
from src.api.model.pagination import PaginationResponse
class CharacterDB(BaseDB):
    __tablename__ = "characters"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, doc="角色唯一标识符。")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False, doc="关联的用户 ID。")
    name = Column(String(256), index=True, unique=True,nullable=False, doc="角色名称。")
    sex = Column(String(256), index=True,nullable=True, doc="角色性别。")
    age = Column(Integer, index=True, nullable=True, doc="角色年龄")
    job = Column(String(256), index=True, nullable=True, doc="角色的工作")
    hobby = Column(String(256), index=True, nullable=True, doc="角色的爱好")
    system_prompt = Column(String(1024), index=True, nullable=True, doc="角色的系统提示词。")
    voice = Column(String(15), nullable=True, doc="角色语音")
    style = Column(String(15), nullable=True, doc="角色图像风格")
    avatars = Column(JSON, nullable=True, doc="角色的头像信息。")
    topics = Column(JSON, nullable=True, doc="角色的话题信息。")
    likes = Column(Integer, default=0, index=True, nullable=True, doc="角色的点赞数量。")
    visibility = Column(Boolean, index=True, nullable=True, doc="角色的可见性状态，True 表示公开，False 表示私有。")
    # background = Column(String(1024), nullable=True, doc="角色背景信息。")
    tts = Column(String(256), nullable=True, doc="角色的文本转语音配置。")
    data = Column(JSON, nullable=True, doc="存储额外元数据的 JSON 字段。")


async def create_character(db: AsyncSession,user_id:str , character: CharacterRequest):
    db_character = CharacterDB(id=uuid.uuid4(),user_id=user_id,**character.model_dump(exclude={"id"}))
    db.add(db_character)
    await db.commit()
    await db.refresh(db_character)
    return db_character

async def delete_character(db: AsyncSession,user_id:str , character_id: str):
    async with db.begin():
        result = await db.execute(
            select(CharacterDB).filter(CharacterDB.user_id == user_id,CharacterDB.id == character_id)
        )
        db_character = result.scalars().first()

        if not db_character:
            return False  
        db_character.is_deleted = True
        await db.commit()

        return True

async def edit_character(db: AsyncSession ,user_id:str,character: CharacterRequest):
    async with db.begin():
        result = await db.execute(select(CharacterDB).filter(CharacterDB.user_id == user_id,CharacterDB.id == character.id))
        db_character = result.scalars().first()

        if not db_character:
            return None  
        character_data = character.model_dump(exclude={"id", "user_id"})
        for key, value in character_data.items():
            if hasattr(db_character, key) and value is not None and value != "":
                setattr(db_character, key, value)
        await db.commit()
        return db_character
async def get_character_by_name(db: AsyncSession, character_name: str):
    async with db.begin():
        result = await db.execute(select(CharacterDB).filter(CharacterDB.name == character_name))
        return result.scalars().first()
    
async def get_character_by_id(db: AsyncSession, character_id: str):
    async with db.begin():
        result = await db.execute(select(CharacterDB).filter(CharacterDB.id == character_id))
        return result.scalars().first()

async def get_character_list(db: AsyncSession, characterList: CharacterListRequest,user_id: str=None) -> PaginationResponse[dict]:
    base_query = select(CharacterDB)

    if hasattr(characterList, 'visibility') and characterList.visibility:
        base_query = base_query.filter(CharacterDB.visibility == characterList.visibility)
    if user_id:
        base_query = base_query.filter(CharacterDB.user_id == user_id)

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

