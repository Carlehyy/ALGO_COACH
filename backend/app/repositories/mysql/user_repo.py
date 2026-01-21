"""
ACM算法学习平台 - UserRepository
用户数据访问层
参考：开发指南V3 - Repository层示例
"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mysql.user import User
from loguru import logger


class UserRepository:
    """用户数据访问类"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """创建用户"""
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        logger.info(f"[UserRepo] 创建用户: id={user.id}, email={user.email}")
        return user

    async def update(self, user: User) -> User:
        """更新用户"""
        await self.db.flush()
        await self.db.refresh(user)
        logger.info(f"[UserRepo] 更新用户: id={user.id}")
        return user

    async def delete(self, user: User) -> None:
        """删除用户（软删除，设置为禁用状态）"""
        user.status = "0"  # 设置为禁用
        await self.db.flush()
        logger.info(f"[UserRepo] 禁用用户: id={user.id}")

    async def exists_by_email(self, email: str) -> bool:
        """检查邮箱是否存在"""
        result = await self.db.execute(
            select(User.id).where(User.email == email).limit(1)
        )
        return result.scalar_one_or_none() is not None

    async def update_last_login(self, user: User) -> None:
        """更新最后登录时间"""
        from datetime import datetime
        user.last_login_at = datetime.utcnow()
        await self.db.flush()

    async def add_points(self, user: User, points: int) -> User:
        """增加积分"""
        user.points += points
        await self.db.flush()
        logger.info(f"[UserRepo] 用户积分变更: id={user.id}, +{points}, 当前余额={user.points}")
        return user

    async def consume_points(self, user: User, points: int) -> User:
        """消费积分"""
        if user.points < points:
            raise ValueError("积分不足")
        user.points -= points
        user.total_consumed += points
        await self.db.flush()
        logger.info(f"[UserRepo] 用户积分消费: id={user.id}, -{points}, 当前余额={user.points}")
        return user

    async def recharge_points(self, user: User, points: int) -> User:
        """充值积分"""
        user.points += points
        user.total_recharged += points
        await self.db.flush()
        logger.info(f"[UserRepo] 用户积分充值: id={user.id}, +{points}, 当前余额={user.points}")
        return user

    async def list_users(
        self,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
        role: Optional[str] = None,
    ) -> tuple[list[User], int]:
        """
        获取用户列表

        返回: (用户列表, 总数)
        """
        query = select(User)

        # 筛选条件
        if status:
            query = query.where(User.status == status)
        if role:
            query = query.where(User.role == role)

        # 获取总数
        count_query = select(User.id)
        if status:
            count_query = count_query.where(User.status == status)
        if role:
            count_query = count_query.where(User.role == role)

        count_result = await self.db.execute(count_query)
        total = len(count_result.all())

        # 分页
        query = query.offset(skip).limit(limit)
        query = query.order_by(User.id.desc())

        result = await self.db.execute(query)
        users = result.scalars().all()

        return list(users), total
