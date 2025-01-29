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

async def create_session(db: AsyncSession,user_id:str,session: SessionRequest):
    db_session = SessionDB(user_id=user_id,**session.model_dump(exclude={"id"}))
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    return db_session

async def edit_session(db: AsyncSession,user:UserDB ,session: SessionRequest):
    async with db.begin():
        result = await db.execute(select(SessionDB).filter(SessionDB.user_id==user.id,SessionDB.character_id==session.character_id))
        db_session = result.scalars().first()

        if not db_session:
            return None  
        session_data = session.model_dump(include={"user_id", "character_id"})
        for key, value in session_data.items():
            if hasattr(db_session, key) and value is not None and value != "":
                setattr(db_session, key, value)
        await db.commit()
        return db_session

async def delete_session(db: AsyncSession,user_id:str, character_id: str):
     async with db.begin():
        result = await db.execute(
            select(SessionDB).filter(SessionDB.user_id==user_id,SessionDB.character_id == character_id)
        )
        db_session = result.scalars().first()

        if not db_session:
            return False  
        db_session.is_deleted = True
        await db.commit()

        return True
    
async def get_session_by_id(db: AsyncSession,user_id:str, character_id: str):
    async with db.begin():
        result = await db.execute(select(SessionDB).filter(SessionDB.user_id == user_id,SessionDB.character_id == character_id))
        return result.scalars().first()
    
from sqlalchemy.orm import aliased, load_only
from sqlalchemy import select, func
from math import ceil


async def get_session_list(db: AsyncSession, user_id: str, sessionList: SessionListRequest) -> PaginationResponse[dict]:
    # 创建 characters 表的别名
    CharacterAlias = aliased(CharacterDB)

    # 基础查询，关联 sessions 表和 characters 表
    base_query = select(
        SessionDB.id,
        SessionDB.user_id,
        SessionDB.character_id,
        SessionDB.new_message,
        SessionDB.created_at,
        SessionDB.updated_at,
        CharacterAlias.name.label("character_name"),
        CharacterAlias.avatars.label("character_avatars")
    ).join(
        CharacterAlias,
        SessionDB.character_id == CharacterAlias.id,
        isouter=True  # 使用 LEFT JOIN，确保即使没有匹配的 characters 记录，sessions 记录仍然会被返回
    )

    # 根据 character_id 过滤
    if sessionList.character_id is not None:
        base_query = base_query.filter(SessionDB.character_id == sessionList.character_id)
    if user_id:
        base_query = base_query.filter(SessionDB.user_id == user_id)

    count_query = base_query.with_only_columns(func.count()).order_by(None)
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    offset = (sessionList.page - 1) * sessionList.page_size
    paginated_query = base_query.offset(offset).limit(sessionList.page_size)

    result = await db.execute(paginated_query)
    records = result.all()  # 使用 .all() 而不是 .scalars().all()

    total_pages = ceil(total / sessionList.page_size) if total > 0 else 0

    # 使用 ._asdict() 将 Row 对象转换为字典
    response_records = [record._asdict() for record in records]
    
    # 移除 SQLAlchemy 内部状态（如果有）
    for record in response_records:
        record.pop('_sa_instance_state', None)

    return PaginationResponse[dict](
        total=total,
        total_pages=total_pages,
        page=sessionList.page,
        page_size=sessionList.page_size,
        records=response_records,
    )
