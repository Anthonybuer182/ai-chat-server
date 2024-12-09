import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer,String

from src.database.postgre.model.base import BaseDB
from src.http.model.character import CharacterRequest
class CharacterDB(BaseDB):
    __tablename__ = "characters"
    id = Column(String(36), primary_key=True, index=True, nullable=False, doc="角色唯一标识符。")
    user_id = Column(String(36), ForeignKey("users.id"), index=True, nullable=False, doc="关联的用户 ID。")
    name = Column(String(256), index=True, unique=True,nullable=False, doc="角色名称。")
    background = Column(String(1024), nullable=True, doc="角色背景信息。")
    portrait = Column(String(256), nullable=True, doc="角色头像的 URL。")
    voice_id = Column(String(15), nullable=True, doc="角色语音的 ID。")
    system_prompt = Column(String(512), index=True, nullable=False, doc="角色的系统提示词。")
    user_prompt = Column(String(512), index=True, nullable=False, doc="用户输入提示词。")
    tts = Column(String(256), nullable=False, doc="角色的文本转语音配置。")
    visibility = Column(Boolean, index=True, nullable=False, doc="角色的可见性状态，True 表示公开，False 表示私有。")
    data = Column(JSON, nullable=True, doc="存储额外元数据的 JSON 字段。")
    likes = Column(Integer, default=0, nullable=False, doc="角色的点赞数量。")

async def get_char_by_name(db: AsyncSession, character_name: str):
    async with db.begin():
        result = await db.execute(select(CharacterDB).filter(CharacterDB.name == character_name))
        return result.scalars().first()
    
async def get_char_by_id(db: AsyncSession, character_id: str):
    async with db.begin():
        result = await db.execute(select(CharacterDB).filter(CharacterDB.id == character_id))
        return result.scalars().first()

async def create_char(db: AsyncSession,user_id: str, character: CharacterRequest):
    db_character = CharacterDB(id=str(uuid.uuid4().hex),user_id=user_id,**character.model_dump(exclude={"id"}))
    db.add(db_character)
    await db.commit()
    await db.refresh(db_character)
    return db_character
async def edit_char(db: AsyncSession, user_id: str, character: CharacterRequest):
    async with db.begin():
        result = await db.execute(select(CharacterDB).filter(CharacterDB.id == character.id, CharacterDB.user_id == user_id))
        db_character = result.scalars().first()

        if not db_character:
            return None  
        character_data = character.model_dump(exclude={"id", "user_id"})
        for key, value in character_data.items():
            if hasattr(db_character, key):
                setattr(db_character, key, value)
        await db.commit()
        return db_character
