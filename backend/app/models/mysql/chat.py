"""
ACM算法学习平台 - AI教练 SQLite模型
使用SQLite存储聊天会话和消息
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, BigInteger, DateTime, Enum
from sqlalchemy.orm import declarative_base

# 使用SQLite的Base
try:
    from app.infrastructure.database.sqlite import Base
except ImportError:
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()


class ChatSessionStatus(str, Enum):
    """会话状态枚举"""
    ACTIVE = "active"
    CLOSED = "closed"


class ChatSession(Base):
    """聊天会话表"""
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="会话ID")
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    title = Column(String(200), nullable=False, default="新对话", comment="会话标题")
    topic_id = Column(Integer, nullable=True, comment="关联知识点ID")
    message_count = Column(Integer, default=0, comment="消息数量")
    total_tokens = Column(Integer, default=0, comment="总tokens数")
    status = Column(String(20), default=ChatSessionStatus.ACTIVE, comment="状态")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")


class ChatMessage(Base):
    """聊天消息表"""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="消息ID")
    session_id = Column(Integer, nullable=False, index=True, comment="会话ID")
    role = Column(String(20), nullable=False, comment="角色: user/assistant")
    content = Column(Text, nullable=False, comment="消息内容")
    tokens = Column(Integer, default=0, comment="tokens数")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
