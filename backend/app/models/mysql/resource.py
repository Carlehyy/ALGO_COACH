"""
ACM算法学习平台 - Resource模型
参考：PRD V4 - 10.数据库设计 - t_resource表
"""

import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, Text, DateTime, Enum
from sqlalchemy.orm import declarative_base

from app.infrastructure.database.mysql import Base


class ResourceType(str, enum.Enum):
    """资源类型枚举"""
    PDF = "pdf"
    VIDEO = "video"
    BLOG = "blog"
    LEETCODE = "leetcode"


class ProcessStatus(str, enum.Enum):
    """处理状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ReviewStatus(str, enum.Enum):
    """审核状态枚举"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Resource(Base):
    """资源表模型"""

    __tablename__ = "t_resource"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="资源ID")
    type = Column(String(20), nullable=False, comment="类型(pdf/video/blog/leetcode)")
    title = Column(String(200), nullable=False, comment="标题")
    url = Column(String(500), nullable=True, comment="原始URL")
    file_path = Column(String(500), nullable=True, comment="MinIO文件路径")
    file_size = Column(BigInteger, nullable=True, comment="文件大小(字节)")

    # 处理状态
    process_status = Column(String(20), default=ProcessStatus.PENDING, nullable=False, comment="处理状态")
    review_status = Column(String(20), default=ReviewStatus.PENDING, nullable=False, comment="审核状态")

    # 上传者信息
    uploader_id = Column(Integer, nullable=False, index=True, comment="上传者ID")

    # 元数据
    resource_metadata = Column(Text, nullable=True, comment="元数据(JSON)")

    # 解析结果
    parse_result = Column(Text, nullable=True, comment="解析结果(JSON)")

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    processed_at = Column(DateTime, nullable=True, comment="处理完成时间")

    def __repr__(self):
        return f"<Resource(id={self.id}, type={self.type}, title={self.title})>"

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "url": self.url,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "process_status": self.process_status,
            "review_status": self.review_status,
            "uploader_id": self.uploader_id,
            "metadata": self.metadata,
            "parse_result": self.parse_result,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
        }
