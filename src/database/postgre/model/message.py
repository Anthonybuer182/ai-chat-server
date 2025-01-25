from sqlalchemy import (
    Column, String, ForeignKey, Text, Integer, Index
)
from sqlalchemy.dialects.postgresql import UUID, ENUM
from src.database.postgre.model.base import BaseDB

# 定义 ENUM 类型
PlatformEnum = ENUM("web", "android", "ios", "wechat", name="platform_enum")

class MessageDB(BaseDB):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, doc="消息唯一标识符")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, doc="关联用户id")
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, doc="关联角色id")
    platform = Column(PlatformEnum, nullable=False, doc="客户端平台")
    language = Column(String(8), nullable=False, default="en", doc="聊天消息的语言（ISO 639-1 代码）")
    model = Column(String(32), nullable=False, doc="模型名称")
    request_id = Column(String(48), index=True, nullable=True, doc="API 请求 ID")
    role = Column(String(16), nullable=False, doc="消息角色（如 user/assistant/system）")
    content = Column(Text, nullable=True, doc="消息内容")
    finish_reason = Column(String(128), nullable=True, doc="完成原因")
    prompt_tokens = Column(Integer, nullable=True, doc="提示词数")
    completion_tokens = Column(Integer, nullable=True, doc="完成词数")
    total_tokens = Column(Integer, nullable=True, doc="总词数")

    # 定义索引
    __table_args__ = (
        Index('idx_user_character', 'user_id', 'character_id'),  # 联合索引
        Index('idx_platform', 'platform'),  # platform 字段索引
        Index('idx_model', 'model'),  # model 字段索引
        Index('idx_language', 'language'),  # language 字段索引
    )

    def __repr__(self):
        return f"<MessageDB(id={self.id}, user_id={self.user_id}, character_id={self.character_id}, platform={self.platform}, language={self.language}, model={self.model}, role={self.role}, content={self.content[:20]}...)>"