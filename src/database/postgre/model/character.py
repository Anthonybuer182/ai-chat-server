import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer,String

from src.database.postgre.model.base import BaseDB
class Character(BaseDB):
    __tablename__ = "characters"
    id = Column(String(36), primary_key=True, index=True, nullable=False, doc="角色唯一标识符。")
    user_id = Column(String(36), ForeignKey("users.id"), index=True, nullable=False, doc="关联的用户 ID。")
    name = Column(String(256), index=True, unique=True,nullable=False, doc="角色名称。")
    background = Column(String(1024), nullable=True, doc="角色背景信息。")
    voice_id = Column(String(15), nullable=True, doc="角色语音的 ID。")
    system_prompt = Column(String(512), index=True, nullable=False, doc="角色的系统提示词。")
    user_prompt = Column(String(512), index=True, nullable=False, doc="用户输入提示词。")
    tts = Column(String(256), nullable=False, doc="角色的文本转语音配置。")
    visibility = Column(Boolean, index=True, nullable=False, doc="角色的可见性状态，True 表示公开，False 表示私有。")
    data = Column(JSON, nullable=True, doc="存储额外元数据的 JSON 字段。")
    likes = Column(Integer, default=0, nullable=False, doc="角色的点赞数量。")

async def get_character_by_name(db: AsyncSession, character_name: str):
    async with db.begin():
        result = await db.execute(select(Character).filter(Character.name == character_name))
        return result.scalars().first()
    
async def get_caracter_by_id(db: AsyncSession, character_id: str):
    async with db.begin():
        result = await db.execute(select(Character).filter(Character.id == character_id))
        return result.scalars().first()

async def create_character(db: AsyncSession, name: str, password: str, phone: str, email: str):
    db_character = Character(id=str(uuid.uuid4().hex),name=name)
    db.add(db_character)
    await db.commit()
    await db.refresh(db_character)
    return db_character