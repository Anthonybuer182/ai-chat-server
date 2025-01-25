from sqlalchemy import JSON, Column, ForeignKey, Index, String, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from src.database.postgre.model.base import BaseDB

class SessionDB(BaseDB):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True, doc="自增主键")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False, doc="关联的用户ID")
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id", ondelete="CASCADE"), index=True, nullable=False, doc="角色ID")
    character_name = Column(String(64), index=True, nullable=False, doc="角色名称")
    character_avatar = Column(String(256), nullable=True, doc="角色头像")
    new_message = Column(Text, nullable=True, doc="最新消息")
    messages_context = Column(JSON, nullable=True, doc="历史消息上下文（JSON 格式）")

    __table_args__ = (
        Index('ix_user_character', "user_id", "character_id"),
    )