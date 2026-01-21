"""
ACM算法学习平台 - Note模型 (MongoDB)
参考：开发指南V3 - 6.8 MongoDB模型示例
"""

from datetime import datetime
from typing import Optional, List
from beanie import Document
from pydantic import Field


class Note(Document):
    """笔记文档模型"""

    # 基本信息
    topic_id: str = Field(..., description="关联知识点ID")
    title: str = Field(..., description="标题")
    summary: Optional[str] = Field(None, description="摘要")

    # L1-L4分层内容
    content_l1: Optional[str] = Field(None, description="L1直观引入")
    content_l2: Optional[str] = Field(None, description="L2核心原理")
    content_l3: Optional[str] = Field(None, description="L3代码实现")
    content_l4: Optional[str] = Field(None, description="L4实战分析")

    # 完整内容
    full_content: Optional[str] = Field(None, description="完整Markdown内容")

    # 版本信息
    version: int = Field(default=1, description="版本号")

    # 来源
    sources: List[str] = Field(default_factory=list, description="内容来源ID列表")

    # 质量评分
    quality_score: Optional[float] = Field(None, description="AI质量评分(0-100)")

    # 状态: 0草稿 1待审核 2已发布 3下架
    status: int = Field(default=0, description="状态")

    # 浏览次数
    view_count: int = Field(default=0, description="浏览次数")

    # 时间戳
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = Field(None, description="发布时间")

    # 设置集合名称
    class Settings:
        name = "notes"
        indexes = [
            "topic_id",
            "status",
            "created_at",
        ]

    @property
    def is_published(self) -> bool:
        """是否已发布"""
        return self.status == 2
