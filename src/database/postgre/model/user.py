import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from sqlalchemy import Column,String
from sqlalchemy.dialects.postgresql import UUID, ENUM
from src.database.postgre.model.base import BaseDB
from src.api.model.user import UserRequest
class UserDB(BaseDB):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True),primary_key=True,index=True,nullable=False)
    username = Column(String(256),index=True,unique=True,nullable=False)
    password = Column(String(1024),nullable=False)
    phone = Column(String(15),index=True,nullable=True) 
    email = Column(String(256),index=True,nullable=True)
    avatar = Column(String(1024),index=True,nullable=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_name(db: AsyncSession, username: str):
    async with db.begin():
        result = await db.execute(select(UserDB).filter(UserDB.username == username))
        return result.scalars().first()
    
async def get_user_by_id(db: AsyncSession, user_id: str):
    async with db.begin():
        result = await db.execute(select(UserDB).filter(UserDB.id == user_id))
        return result.scalars().first()

async def create_user(db: AsyncSession, user:UserRequest):
    db_user = UserDB(id=uuid.uuid4(),password=password_hash(user.password),**user.model_dump(exclude={"id","password","code"}))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def edit_user(db: AsyncSession, user: UserRequest):
    async with db.begin():
        result = await db.execute(select(UserDB).filter(UserDB.id == user.id))
        db_user = result.scalars().first()
        if not db_user:
            return None  
        user_data = user.model_dump(exclude={"id"})
        for key, value in user_data.items():
            if hasattr(db_user, key) and value is not None and value != "":
                if key == "password":
                    encrypted_password = password_hash(value.encode())
                    setattr(db_user, key, encrypted_password)
                else:
                    setattr(db_user, key, value)
        await db.commit()
        return db_user

async def delete_user(db: AsyncSession, user_id: str):
    async with db.begin():
        result = await db.execute(
            select(UserDB).filter(UserDB.id == user_id)
        )
        db_user = result.scalars().first()

        if not db_user:
            return False  
        db_user.is_deleted = True
        await db.commit()

        return True
    
def password_hash(password):
    return pwd_context.hash(password)
def verify_password(origin_password, hashed_password):
    return pwd_context.verify(origin_password, hashed_password)

