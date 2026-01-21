"""
ACM算法学习平台 - UserService
用户业务逻辑层
参考：开发指南V3 - 6.9 Service层示例
"""

from typing import Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mysql.user import User, UserRole
from app.repositories.mysql.user_repo import UserRepository
from app.api.v1.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import BusinessException, ErrorCode
from loguru import logger


class UserService:
    """用户业务逻辑类"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def create_user(self, user_in: UserCreate) -> User:
        """
        创建用户（注册）

        Args:
            user_in: 用户创建信息

        Returns:
            创建的用户对象

        Raises:
            BusinessException: 邮箱已存在
        """
        # 检查邮箱是否已存在
        existing_user = await self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise BusinessException(*ErrorCode.USER_EXISTS)

        # 创建用户
        user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            nickname=user_in.nickname or user_in.email.split("@")[0],
            points=100,  # 新用户赠送100积分
        )

        user = await self.user_repo.create(user)
        await self.db.commit()

        logger.info(f"[UserService] 用户注册成功: id={user.id}, email={user.email}")
        return user

    async def authenticate(self, email: str, password: str) -> Dict:
        """
        用户认证（登录）

        Args:
            email: 邮箱
            password: 密码

        Returns:
            包含用户和Token的字典

        Raises:
            BusinessException: 用户不存在、密码错误、用户已禁用
        """
        # 获取用户
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise BusinessException(*ErrorCode.USER_NOT_FOUND)

        # 验证密码
        if not verify_password(password, user.hashed_password):
            raise BusinessException(*ErrorCode.PASSWORD_ERROR)

        # 检查用户状态
        if not user.is_active:
            raise BusinessException(*ErrorCode.USER_DISABLED)

        # 更新最后登录时间
        await self.user_repo.update_last_login(user)
        await self.db.commit()

        # 生成Token
        access_token = create_access_token(str(user.id))

        logger.info(f"[UserService] 用户登录成功: id={user.id}, email={user.email}")
        return {
            "user": user,
            "access_token": access_token,
        }

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return await self.user_repo.get_by_id(user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return await self.user_repo.get_by_email(email)

    async def update_user(self, user: User, user_in: UserUpdate) -> User:
        """
        更新用户信息

        Args:
            user: 用户对象
            user_in: 更新数据

        Returns:
            更新后的用户对象
        """
        # 更新字段
        if user_in.nickname is not None:
            user.nickname = user_in.nickname
        if user_in.avatar is not None:
            user.avatar = user_in.avatar
        if user_in.leetcode_username is not None:
            user.leetcode_username = user_in.leetcode_username

        user = await self.user_repo.update(user)
        await self.db.commit()

        logger.info(f"[UserService] 更新用户信息: id={user.id}")
        return user

    async def change_password(
        self, user: User, old_password: str, new_password: str
    ) -> None:
        """
        修改密码

        Args:
            user: 用户对象
            old_password: 旧密码
            new_password: 新密码

        Raises:
            BusinessException: 旧密码错误
        """
        # 验证旧密码
        if not verify_password(old_password, user.hashed_password):
            raise BusinessException(10001, "旧密码错误")

        # 更新密码
        user.hashed_password = get_password_hash(new_password)
        await self.user_repo.update(user)
        await self.db.commit()

        logger.info(f"[UserService] 用户修改密码: id={user.id}")

    async def update_points(
        self, user: User, points_change: int, reason: str
    ) -> User:
        """
        更新用户积分

        Args:
            user: 用户对象
            points_change: 积分变化量（正数增加，负数减少）
            reason: 变动原因

        Returns:
            更新后的用户对象

        Raises:
            BusinessException: 积分不足
        """
        if points_change > 0:
            user = await self.user_repo.add_points(user, points_change)
        else:
            user = await self.user_repo.consume_points(user, -points_change)

        await self.db.commit()
        logger.info(
            f"[UserService] 用户积分变动: id={user.id}, 变动={points_change}, 原因={reason}"
        )
        return user

    async def list_users(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        role: Optional[str] = None,
    ) -> tuple[list[User], int]:
        """
        获取用户列表

        Args:
            page: 页码（从1开始）
            page_size: 每页数量
            status: 状态筛选
            role: 角色筛选

        Returns:
            (用户列表, 总数)
        """
        skip = (page - 1) * page_size
        users, total = await self.user_repo.list_users(
            skip=skip, limit=page_size, status=status, role=role
        )
        return users, total

    async def disable_user(self, user_id: int) -> None:
        """
        禁用用户

        Args:
            user_id: 用户ID
        """
        user = await self.get_by_id(user_id)
        if user:
            await self.user_repo.delete(user)
            await self.db.commit()
            logger.info(f"[UserService] 禁用用户: id={user_id}")

    async def get_user_balance(self, user: User) -> Dict:
        """
        获取用户积分余额信息

        Args:
            user: 用户对象

        Returns:
            积分信息字典
        """
        return {
            "points": user.points,
            "total_recharged": user.total_recharged,
            "total_consumed": user.total_consumed,
        }
