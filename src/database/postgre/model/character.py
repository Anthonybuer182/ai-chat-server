from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer,String
from sqlalchemy.dialects.postgresql import UUID
from src.database.postgre.model.base import BaseDB

class CharacterDB(BaseDB):
    __tablename__ = "characters"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, doc="角色唯一标识符。")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False, doc="关联的用户 ID。")
    name = Column(String(256), index=True, unique=True,nullable=False, doc="角色名称。")
    sex = Column(String(256), index=True,nullable=True, doc="角色性别。")
    age = Column(Integer, index=True, nullable=True, doc="角色年龄")
    job = Column(String(256), index=True, nullable=True, doc="角色的工作")
    hobby = Column(String(256), index=True, nullable=True, doc="角色的爱好")
    system_prompt = Column(String(1024), index=True, nullable=True, doc="角色的系统提示词。")
    voice = Column(String(15), nullable=True, doc="角色语音")
    style = Column(String(15), nullable=True, doc="角色图像风格")
    avatars = Column(JSON, nullable=True, doc="角色的头像信息。")
    topics = Column(JSON, nullable=True, doc="角色的话题信息。")
    likes = Column(Integer, default=0, index=True, nullable=True, doc="角色的点赞数量。")
    visibility = Column(Boolean, index=True, nullable=True, doc="角色的可见性状态，True 表示公开，False 表示私有。")
    # background = Column(String(1024), nullable=True, doc="角色背景信息。")
    tts = Column(String(256), nullable=True, doc="角色的文本转语音配置。")
    data = Column(JSON, nullable=True, doc="存储额外元数据的 JSON 字段。")


