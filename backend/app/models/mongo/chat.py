"""
ChatSession和ChatMessage模型 (MongoDB)
"""

from datetime import datetime
from typing import List, Optional
from beanie import Document, PydanticObjectId
from pydantic import Field


class ChatMessage(Document):
    """聊天消息文档模型"""

    session_id: PydanticObjectId = Field(..., description="会话ID")
    role: str = Field(..., description="角色(user/assistant)")
    content: str = Field(..., description="消息内容")
    tokens: int = Field(default=0, description="Token数量")
    cost: float = Field(default=0.0, description="成本(元)")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "chat_messages"
        indexes = [
            "session_id",
            "created_at",
        ]


class ChatSession(Document):
    """聊天会话文档模型"""

    user_id: int = Field(..., description="用户ID")
    title: str = Field(..., description="会话标题")
    topic_id: Optional[str] = Field(None, description="关联知识点ID")
    message_count: int = Field(default=0, description="消息数量")
    total_tokens: int = Field(default=0, description="总Token消耗")
    total_cost: float = Field(default=0.0, description="总成本")
    status: str = Field(default="active", description="状态(active/closed)")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "chat_sessions"
        indexes = [
            "user_id",
            "status",
            "created_at",
        ]
