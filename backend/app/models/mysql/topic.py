"""
ACM算法学习平台 - Topic模型
参考：PRD V4 - 10.数据库设计 - t_topic表
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, JSON
from sqlalchemy.orm import declarative_base

from app.infrastructure.database.mysql import Base


class Topic(Base):
    """知识点表模型"""

    __tablename__ = "t_topic"

    # 主键（字符串ID，如binary_search）
    id = Column(String(100), primary_key=True, comment="知识点ID")

    # 基本信息
    name = Column(String(100), nullable=False, comment="名称")
    name_en = Column(String(100), nullable=False, comment="英文名")
    category = Column(String(50), nullable=False, index=True, comment="分类")
    difficulty = Column(Integer, nullable=False, default=1, comment="难度(1-5)")
    importance = Column(Integer, nullable=False, default=1, comment="重要性(1-5)")

    # 关联关系（JSON格式）
    prerequisites = Column(JSON, nullable=True, comment="前置知识点ID列表")
    related = Column(JSON, nullable=True, comment="相关知识点ID列表")

    # 描述信息
    description = Column(Text, nullable=True, comment="描述")
    estimated_hours = Column(Integer, default=0, comment="预计学习时长(小时)")

    # 状态
    status = Column(String(1), default="1", nullable=False, comment="状态(0禁用 1正常)")

    # 时间戳
    created_at = Column(String(50), nullable=False, comment="创建时间")
    updated_at = Column(String(50), nullable=False, comment="更新时间")

    def __repr__(self):
        return f"<Topic(id={self.id}, name={self.name}, category={self.category})>"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "category": self.category,
            "difficulty": self.difficulty,
            "importance": self.importance,
            "prerequisites": self.prerequisites or [],
            "related": self.related or [],
            "description": self.description,
            "estimated_hours": self.estimated_hours,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
