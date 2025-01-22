from sqlalchemy import (
    Column, String, ForeignKey, Text, Integer, Index
)
from sqlalchemy.dialects.postgresql import UUID, ENUM
from src.database.postgre.model.base import BaseDB
class MessageDB(BaseDB):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, doc="消息唯一标识符")
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), index=True, nullable=False, doc="关联会话ID")
    platform = Column(ENUM("web", "android", "ios", "MiniProgram", name="platform_enum"), index=True, nullable=False, doc="客户端平台")
    language = Column(String(8), index=True, nullable=False, default="en", doc="聊天消息的语言（ISO 639-1 代码）")
    model = Column(String(32), index=True, nullable=False, doc="模型名称")
    request_id = Column(String(48), index=True, nullable=True, doc="API 请求 ID")
    role = Column(String(16), nullable=False, doc="消息角色（如 user/assistant/system）")
    content = Column(Text, nullable=True, doc="消息内容")
    finish_reason = Column(String(128), nullable=True, doc="完成原因")
    prompt_tokens = Column(Integer, nullable=True, doc="提示词数")
    completion_tokens = Column(Integer, nullable=True, doc="完成词数")
    total_tokens = Column(Integer, nullable=True, doc="总词数")
    
    __table_args__ = (
        Index('ix_session_platform', "session_id", "platform"),
    )

    

    

