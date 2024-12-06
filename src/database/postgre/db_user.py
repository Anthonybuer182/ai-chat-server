import uuid
from src.database.postgre.db_base import Base
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from sqlalchemy import Column,String
class User(Base):
    __tablename__ = "users"
    id = Column(String(36),primary_key=True,index=True,nullable=False)
    username = Column(String(256),index=True,nullable=False)
    password = Column(String(1024),nullable=False)
    phone = Column(String(15),index=True,nullable=False) 
    email = Column(String(256),index=True,nullable=False) 
    # class Config:
    #     from_attributes = True
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
async def get_user(db: AsyncSession, username: str):
    async with db.begin():
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

async def create_user(db: AsyncSession, username: str, password: str, phone: str, email: str):
    db_user = User(id=str(uuid.uuid4().hex),username=username,password=password_hash(password),phone=phone,email=email)
    db_user.phone = phone
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
def password_hash(password):
    return pwd_context.hash(password)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)