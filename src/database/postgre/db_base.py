from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime, Boolean
Base = declarative_base()

class BaseDBModel(Base):
    __abstract__ = True  # 这意味着BaseModel不会在数据库中创建表

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    @validates('updated_at')
    def validate_updated_at(self, key, value):
        return func.now() if value is None else value