"""
ACM算法学习平台 - User模型
参考：开发指南V3 - 6.8 MySQL模型示例
PRD V4 - 10.数据库设计 - t_user表
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric
from sqlalchemy.orm import declarative_base
import enum

from app.infrastructure.database.mysql import Base


class UserRole(str, enum.Enum):
    """用户角色枚举"""
    USER = "user"
    ADMIN = "admin"


class UserStatus(str, enum.Enum):
    """用户状态枚举"""
    DISABLED = "0"
    ACTIVE = "1"


class User(Base):
    """用户表模型"""

    __tablename__ = "t_user"

    # 主键
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="用户ID")

    # 基本信息
    email = Column(String(255), unique=True, index=True, nullable=False, comment="邮箱")
    hashed_password = Column(String(255), nullable=False, comment="密码哈希")
    nickname = Column(String(100), nullable=True, comment="昵称")
    avatar = Column(String(500), nullable=True, comment="头像URL")

    # 积分信息
    points = Column(Integer, default=0, nullable=False, comment="积分余额")
    total_recharged = Column(Integer, default=0, nullable=False, comment="累计充值积分")
    total_consumed = Column(Integer, default=0, nullable=False, comment="累计消费积分")

    # LeetCode信息
    leetcode_username = Column(String(100), nullable=True, comment="LeetCode用户名")

    # 能力评分
    ability_score = Column(Integer, default=0, nullable=False, comment="能力评分")

    # 状态和角色
    status = Column(String(1), default=UserStatus.ACTIVE, nullable=False, comment="状态(0禁用 1正常)")
    role = Column(String(20), default=UserRole.USER, nullable=False, comment="角色(user/admin)")

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, nickname={self.nickname})>"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "email": self.email,
            "nickname": self.nickname,
            "avatar": self.avatar,
            "points": self.points,
            "total_recharged": self.total_recharged,
            "total_consumed": self.total_consumed,
            "leetcode_username": self.leetcode_username,
            "ability_score": self.ability_score,
            "status": self.status,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
        }

    @property
    def is_active(self):
        """用户是否激活"""
        return self.status == UserStatus.ACTIVE

    @property
    def is_admin(self):
        """用户是否为管理员"""
        return self.role == UserRole.ADMIN
