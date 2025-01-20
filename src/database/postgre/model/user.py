from sqlalchemy import Column,String
from sqlalchemy.dialects.postgresql import UUID
from src.database.postgre.model.base import BaseDB
class UserDB(BaseDB):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True),primary_key=True,index=True,nullable=False)
    username = Column(String(256),index=True,unique=True,nullable=False)
    password = Column(String(1024),nullable=False)
    phone = Column(String(15),index=True,nullable=True) 
    email = Column(String(256),index=True,nullable=True)
    avatar = Column(String(1024),index=True,nullable=True)

