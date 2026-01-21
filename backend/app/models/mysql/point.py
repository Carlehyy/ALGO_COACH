"""
ACM算法学习平台 - 积分流水表模型
参考：PRD V4 - 10.数据库设计 - t_point_log
"""

from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime
from sqlalchemy.orm import declarative_base

from app.infrastructure.database.mysql import Base


class PointLog(Base):
    """积分流水表模型"""

    __tablename__ = "t_point_log"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="流水ID")
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    type = Column(String(20), nullable=False, comment="类型(recharge/consume/refund/gift)")
    amount = Column(Integer, nullable=False, comment="变动数量(正负)")
    balance = Column(Integer, nullable=False, comment="变动后余额")
    reason = Column(String(200), nullable=True, comment="变动原因")
    related_id = Column(String(100), nullable=True, comment="关联ID(订单/会话)")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")

    def __repr__(self):
        return f"<PointLog(id={self.id}, user_id={self.user_id}, amount={self.amount})>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "amount": self.amount,
            "balance": self.balance,
            "reason": self.reason,
            "related_id": self.related_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
