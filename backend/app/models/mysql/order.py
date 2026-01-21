"""
ACM算法学习平台 - 充值订单表模型
参考：PRD V4 - 10.数据库设计 - t_order
"""

from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Enum
from sqlalchemy.orm import declarative_base
import enum

from app.infrastructure.database.mysql import Base


class OrderStatus(str, enum.Enum):
    """订单状态枚举"""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class Order(Base):
    """充值订单表模型"""

    __tablename__ = "t_order"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="订单ID")
    order_no = Column(String(50), unique=True, nullable=False, index=True, comment="订单号")
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    package_id = Column(Integer, nullable=False, comment="套餐ID")
    amount = Column(BigInteger, nullable=False, comment="金额(分)")
    points = Column(Integer, nullable=False, comment="积分数量")
    status = Column(String(20), default=OrderStatus.PENDING, nullable=False, comment="状态")
    pay_channel = Column(String(50), nullable=True, comment="支付渠道")
    paid_at = Column(DateTime, nullable=True, comment="支付时间")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")

    def __repr__(self):
        return f"<Order(id={self.id}, order_no={self.order_no}, status={self.status})>"

    def to_dict(self):
        return {
            "id": self.id,
            "order_no": self.order_no,
            "user_id": self.user_id,
            "package_id": self.package_id,
            "amount": self.amount,
            "points": self.points,
            "status": self.status,
            "pay_channel": self.pay_channel,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @property
    def is_paid(self) -> bool:
        """是否已支付"""
        return self.status == OrderStatus.PAID
