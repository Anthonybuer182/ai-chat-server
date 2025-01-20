from asyncio import futures
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
import os

from config import DATABASE_URL
from src.util.logger import get_logger


engine = create_async_engine(DATABASE_URL, echo=True,future = True)

logger = get_logger(__name__)

async def init_db():
    logger.info(DATABASE_URL)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            if result.fetchone() is not None:
                logger.info("Database connection successful.")
            else:
                logger.info("Database connection failed.")
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        raise e

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
