from math import ceil
import uuid
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from src.api.model.character import CharacterListRequest, CharacterRequest
from src.api.model.pagination import PaginationResponse
from src.database.postgre.model.character import CharacterDB
from src.database.postgre.model.session import SessionDB


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

from sqlalchemy.orm import aliased
from sqlalchemy import select, and_, func
from math import ceil

async def get_character_list(db: AsyncSession, characterList: CharacterListRequest, user_id: str = None) -> PaginationResponse[dict]:
    # 创建 sessions 表的别名
    SessionAlias = aliased(SessionDB)

    # 基础查询，使用 LEFT JOIN 关联 characters 表和 sessions 表
    base_query = select(
        CharacterDB,  # 选择 characters 表的所有字段
        SessionAlias.id.label("session_id")  # 选择 sessions 表的 id 字段
    ).join(
        SessionAlias,
        and_(
            CharacterDB.id == SessionAlias.character_id,
            CharacterDB.user_id == SessionAlias.user_id
        ),
        isouter=True  # 使用 LEFT JOIN
    )

    # 根据 visibility 过滤
    if hasattr(characterList, 'visibility') and characterList.visibility:
        base_query = base_query.filter(CharacterDB.visibility == characterList.visibility)

    # 根据 user_id 过滤
    if user_id:
        base_query = base_query.filter(CharacterDB.user_id == user_id)

    # 计算总数
    count_query = base_query.with_only_columns(func.count()).order_by(None)
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # 分页
    offset = (characterList.page - 1) * characterList.page_size
    paginated_query = base_query.offset(offset).limit(characterList.page_size)

    # 执行查询
    result = await db.execute(paginated_query)
    records = result.all()  # 获取所有记录

    # 计算总页数
    total_pages = ceil(total / characterList.page_size) if total > 0 else 0

    # 将查询结果转换为字典
    response_records = []
    for record in records:
        character_data = record[0].__dict__  # characters 表的数据
        session_data = {
            "session_id": record.session_id if record.session_id else None  # sessions 表的数据，如果没有则为 None
        }
        character_data.update(session_data)  # 合并 characters 和 sessions 的数据
        character_data.pop('_sa_instance_state', None)  # 移除 SQLAlchemy 的内部状态
        response_records.append(character_data)

    # 返回分页响应
    return PaginationResponse[dict](
        total=total,
        total_pages=total_pages,
        page=characterList.page,
        page_size=characterList.page_size,
        records=response_records,
    )

