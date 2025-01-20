from math import ceil
from sre_constants import ANY
import uuid
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from src.database.postgre.model.character import CharacterDB
from src.database.postgre.model.session import SessionDB
from src.database.postgre.model.user import UserDB
from src.api.model.pagination import PaginationResponse
from src.api.model.session import SessionListRequest, SessionRequest

async def create_session(db: AsyncSession,user:UserDB ,session: SessionRequest):
    db_session = SessionDB(id=uuid.uuid4(),user_id=user.id,user_name=user.username,**session.model_dump(exclude={"id"}))
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
    
from sqlalchemy.orm import aliased, load_only
from sqlalchemy import select, func
from math import ceil

async def get_session_list(db: AsyncSession,user_id: str, sessionList: SessionListRequest) -> PaginationResponse[dict]:
    # 创建 characters 表的别名
    CharacterAlias = aliased(CharacterDB)

    # 基础查询，关联 sessions 表和 characters 表
    base_query = select(
        SessionDB.id,
        SessionDB.user_id,
        SessionDB.user_name,
        SessionDB.character_id,
        SessionDB.new_message,
        SessionDB.created_at,
        SessionDB.updated_at,
        CharacterAlias.id.label("character_id"),
        CharacterAlias.name.label("character_name"),
        CharacterAlias.avatars.label("character_avatar")
    ).join(
        CharacterAlias,
        SessionDB.character_id == CharacterAlias.id,
        isouter=True  # 使用 LEFT JOIN，确保即使没有匹配的 characters 记录，sessions 记录仍然会被返回
    )

    # 根据 character_id 过滤
    if sessionList.character_id is not None:
        base_query = base_query.filter(SessionDB.character_id == sessionList.character_id)

    # 根据 user_id 过滤
    if user_id:
        base_query = base_query.filter(SessionDB.user_id == user_id)

    # 计算总数
    count_query = base_query.with_only_columns(func.count()).order_by(None)
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # 分页
    offset = (sessionList.page - 1) * sessionList.page_size
    paginated_query = base_query.offset(offset).limit(sessionList.page_size)

    # 执行查询
    result = await db.execute(paginated_query)
    records = result.all()  # 获取所有记录

    # 计算总页数
    total_pages = ceil(total / sessionList.page_size) if total > 0 else 0

    # 将查询结果转换为字典
    response_records = []
    for record in records:
        session_data = {
            "id": record.id,
            "user_id": record.user_id,
            "user_name": record.user_name,
            "character_id": record.character_id,
            "new_message": record.new_message,
            "created_at": record.created_at,
            "updated_at": record.updated_at,
            "character_name": record.character_name,
            "character_avatar": record.character_avatar
        }
        response_records.append(session_data)

    # 返回分页响应
    return PaginationResponse[dict](
        total=total,
        total_pages=total_pages,
        page=sessionList.page,
        page_size=sessionList.page_size,
        records=response_records,
    )

