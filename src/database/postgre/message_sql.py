from math import ceil
from typing import List
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from src.api.model.message import MessageListRequest, MessageRequest
from src.api.model.pagination import PaginationResponse
from src.database.postgre.model.message import MessageDB
from src.multi_models.llm.model.message import ChatMessage

async def create_message(db: AsyncSession, message: MessageRequest):
    db_message = MessageDB(id=uuid4(),**message.model_dump(exclude={"id"}))
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message

async def create_messages(db: AsyncSession, message: MessageRequest, new_messages: List[ChatMessage]):
    db_messages = [
        MessageDB(
            id=uuid4(),
            session_id=message.session_id,
            platform=message.platform,
            language=message.language,
            model=message.model,
            request_id=chat_message.request_id,
            role=chat_message.role,
            content=chat_message.content,
            finish_reason=chat_message.finish_reason,
            prompt_tokens=chat_message.prompt_tokens,
            completion_tokens=chat_message.completion_tokens,
            total_tokens=chat_message.total_tokens,
            created_at=chat_message.created_at
        )
        for chat_message in new_messages
    ]
    db.add_all(db_messages)
    await db.commit()
    for db_message in db_messages:
        await db.refresh(db_message)

    return db_messages
   

async def edit_message(db: AsyncSession, message: MessageRequest):
    async with db.begin():
        result = await db.execute(select(MessageDB).filter(MessageDB.id == message.id))
        db_message = result.scalars().first()

        if not db_message:
            return None  
        message_data = message.model_dump(exclude={"id", "session_id"})
        for key, value in message_data.items():
            if hasattr(db_message, key) and value is not None and value != "":
                setattr(db_message, key, value)
        await db.commit()
        return db_message
    
async def get_message_by_id(db: AsyncSession, message_id: str):
    async with db.begin():
        result = await db.execute(select(MessageDB).filter(MessageDB.id == message_id))
        return result.scalars().first()

async def get_message_list(db: AsyncSession, messageList: MessageListRequest) -> PaginationResponse[dict]:
    base_query = select(MessageDB)

    if messageList.session_id is not None:
        base_query = base_query.filter(MessageDB.session_id == messageList.session_id)

    count_query = base_query.with_only_columns(func.count()).order_by(None)
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    offset = (messageList.page - 1) * messageList.page_size
    paginated_query = base_query.offset(offset).limit(messageList.page_size)

    result = await db.execute(paginated_query)
    records = result.scalars().all()

    total_pages = ceil(total / messageList.page_size) if total > 0 else 0

    response_records = [record.__dict__ for record in records]
    
    for record in response_records:
        record.pop('_sa_instance_state', None)

    return PaginationResponse[dict](
        total=total,
        total_pages=total_pages,
        page=messageList.page,
        page_size=messageList.page_size,
        records=response_records,
    )

async def get_message_limit(db: AsyncSession, session_id: str, limit: int):
    base_query = select(MessageDB).filter(MessageDB.session_id == session_id).order_by(MessageDB.created_at.desc())
    paginated_query = base_query.limit(limit)
    result = await db.execute(paginated_query)
    records = result.scalars().all()
    return records
    

    

