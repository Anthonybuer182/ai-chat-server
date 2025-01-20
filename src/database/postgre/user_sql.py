import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from src.api.model.user import UserRequest
from src.database.postgre.model.user import UserDB

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

