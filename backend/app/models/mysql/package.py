"""
ACM算法学习平台 - 积分套餐表模型
参考：PRD V4 - 2.2 积分套餐
"""

from sqlalchemy import Column, Integer, BigInteger, String, Text
from sqlalchemy.orm import declarative_base

from app.infrastructure.database.mysql import Base


class Package(Base):
    """积分套餐表模型"""

    __tablename__ = "t_package"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="套餐ID")
    name = Column(String(100), nullable=False, comment="套餐名称")
    price = Column(BigInteger, nullable=False, comment="价格(分)")
    points = Column(Integer, nullable=False, comment="积分数量")
    bonus_points = Column(Integer, default=0, nullable=False, comment="赠送积分")
    description = Column(String(500), nullable=True, comment="描述")
    status = Column(String(1), default="1", nullable=False, comment="状态(0禁用 1正常)")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序")

    def __repr__(self):
        return f"<Package(id={self.id}, name={self.name}, points={self.points})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "points": self.points,
            "bonus_points": self.bonus_points,
            "total_points": self.points + self.bonus_points,
            "description": self.description,
            "status": self.status,
            "sort_order": self.sort_order,
        }
