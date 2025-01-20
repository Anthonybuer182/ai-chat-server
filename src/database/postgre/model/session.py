from sqlalchemy import  JSON, Column, ForeignKey, Index,String, Text
from sqlalchemy.dialects.postgresql import UUID
from src.database.postgre.model.base import BaseDB

class SessionDB(BaseDB):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, doc="会话唯一标识符")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False, doc="关联的用户ID")
    user_name = Column(String(64), index=True, nullable=False, doc="用户名称")
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id", ondelete="CASCADE"), index=True, nullable=False, doc="角色ID")
    new_message = Column(Text, nullable=False, doc="最新消息")
    messages_context = Column(JSON, nullable=False, doc="历史消息上下文（JSON 格式）")

    __table_args__ = (
        Index('ix_user_character', "user_id", "character_id"),
    )


