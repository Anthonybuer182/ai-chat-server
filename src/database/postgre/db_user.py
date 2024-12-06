from typing import Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
class User(BaseModel):
    id: int
    username: str
    password: str
    phone: str 
    email: str 
    class Config:
        from_attributes = True
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
async def get_user(db: AsyncSession, username: str) -> Optional[User]:
    async with db.begin():
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

async def create_user(db: AsyncSession, username: str, password: str, phone: str, email: str)-> User:
    db_user = User(username=username,password=password_hash(password),phone=phone,email=email)
    db_user.phone = phone
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
def password_hash(password):
    return pwd_context.hash(password)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)