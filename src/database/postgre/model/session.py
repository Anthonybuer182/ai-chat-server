from math import ceil
from sre_constants import ANY
import uuid
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import  JSON, Column, ForeignKey, Index,String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from src.database.postgre.model.base import BaseDB
from src.database.postgre.model.character import get_character_by_id
from src.database.postgre.model.user import UserDB
from src.api.model.pagination import PaginationResponse
from src.api.model.session import SessionListRequest, SessionRequest
class SessionDB(BaseDB):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, doc="会话唯一标识符")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False, doc="关联的用户ID")
    user_name = Column(String(64), index=True, nullable=False, doc="用户名称")
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id", ondelete="CASCADE"), index=True, nullable=False, doc="角色ID")
    character_name = Column(String(64), index=True, nullable=False, doc="角色名称")
    character_portrait = Column(String(256), nullable=True, doc="角色头像")
    new_message = Column(Text, nullable=False, doc="最新消息")
    messages_context = Column(JSON, nullable=False, doc="历史消息上下文（JSON 格式）")

    __table_args__ = (
        Index('ix_user_character', "user_id", "character_id"),
    )

async def create_session(db: AsyncSession,user:UserDB ,session: SessionRequest):
    character = await get_character_by_id(db,session.character_id)
    if character is None:
        raise ValueError("Character not found")
    db_session = SessionDB(id=uuid.uuid4(),user_id=user.id,user_name=user.username,character_name=character.name,**session.model_dump(exclude={"id"}))
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    return db_session

async def edit_session(db: AsyncSession,user:UserDB ,session: SessionRequest):
    async with db.begin():
        result = await db.execute(select(SessionDB).filter(SessionDB.user_id==user.id,SessionDB.user_name==user.username,SessionDB.id == session.id))
        db_session = result.scalars().first()

        if not db_session:
            return None  
        session_data = session.model_dump(include={"new_message", "messages_context"})
        for key, value in session_data.items():
            if hasattr(db_session, key) and value is not None and value != "":
                setattr(db_session, key, value)
        await db.commit()
        return db_session

async def delete_session(db: AsyncSession,user_id:str, session_id: str):
     async with db.begin():
        result = await db.execute(
            select(SessionDB).filter(SessionDB.user_id==user_id,SessionDB.id == session_id)
        )
        db_session = result.scalars().first()

        if not db_session:
            return False  
        db_session.is_deleted = True
        await db.commit()

        return True
    
async def get_session_by_id(db: AsyncSession, session_id: str):
    async with db.begin():
        result = await db.execute(select(SessionDB).filter(SessionDB.id == session_id))
        return result.scalars().first()
    
async def get_session_list(db: AsyncSession, sessionList: SessionListRequest) -> PaginationResponse[dict]:
    base_query = select(SessionDB)

    if sessionList.character_id is not None:
        base_query = base_query.filter(SessionDB.character_id == sessionList.character_id)
    if sessionList.user_id:
        base_query = base_query.filter(SessionDB.user_id == sessionList.user_id)

    count_query = base_query.with_only_columns(func.count()).order_by(None)
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    offset = (sessionList.page - 1) * sessionList.page_size
    paginated_query = base_query.offset(offset).limit(sessionList.page_size)

    result = await db.execute(paginated_query)
    records = result.scalars().all()

    total_pages = ceil(total / sessionList.page_size) if total > 0 else 0

    response_records = [record.__dict__ for record in records]
    
    for record in response_records:
        record.pop('_sa_instance_state', None)

    return PaginationResponse[dict](
        total=total,
        total_pages=total_pages,
        page=sessionList.page,
        page_size=sessionList.page_size,
        records=response_records,
    )

