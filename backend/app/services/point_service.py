"""
积分Service业务逻辑层
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import random
import string

from app.models.mysql.user import User
from app.models.mysql.point import PointLog
from app.models.mysql.order import Order, OrderStatus
from app.models.mysql.package import Package
from app.core.exceptions import BusinessException, ErrorCode
from loguru import logger


class PointService:
    """积分业务逻辑类"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_balance(self, user: User) -> dict:
        """获取用户积分余额"""
        return {
            "points": user.points,
            "total_recharged": user.total_recharged,
            "total_consumed": user.total_consumed,
        }

    async def get_logs(
        self, user: User, skip: int = 0, limit: int = 20
    ) -> tuple[List[PointLog], int]:
        """获取积分流水"""
        query = select(PointLog).where(PointLog.user_id == user.id)

        # 获取总数
        count_query = select(PointLog.id).where(PointLog.user_id == user.id)
        count_result = await self.db.execute(count_query)
        total = len(count_result.all())

        # 分页
        query = query.order_by(PointLog.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        logs = result.scalars().all()

        return list(logs), total

    async def check_balance(self, user: User, required_points: int) -> bool:
        """检查积分是否足够"""
        return user.points >= required_points

    async def consume(
        self, user: User, points: int, reason: str, related_id: Optional[str] = None
    ) -> User:
        """消费积分"""
        if user.points < points:
            raise BusinessException(*ErrorCode.POINTS_NOT_ENOUGH)

        # 扣减积分
        user.points -= points
        user.total_consumed += points

        # 记录流水
        log = PointLog(
            user_id=user.id,
            type="consume",
            amount=-points,
            balance=user.points,
            reason=reason,
            related_id=related_id,
        )
        self.db.add(log)

        await self.db.flush()
        logger.info(f"[PointService] 用户积分消费: user_id={user.id}, -{points}")
        return user

    async def recharge(
        self, user: User, points: int, reason: str, related_id: Optional[str] = None
    ) -> User:
        """充值积分（内部方法）"""
        user.points += points
        user.total_recharged += points

        # 记录流水
        log = PointLog(
            user_id=user.id,
            type="recharge",
            amount=points,
            balance=user.points,
            reason=reason,
            related_id=related_id,
        )
        self.db.add(log)

        await self.db.flush()
        logger.info(f"[PointService] 用户积分充值: user_id={user.id}, +{points}")
        return user

    def _generate_order_no(self) -> str:
        """生成订单号"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.choices(string.digits, k=6))
        return f"ORDER{timestamp}{random_str}"

    async def create_order(
        self, user: User, package_id: int
    ) -> Order:
        """创建充值订单"""
        # 获取套餐信息
        result = await self.db.execute(
            select(Package).where(Package.id == package_id, Package.status == "1")
        )
        package = result.scalar_one_or_none()
        if not package:
            raise BusinessException(60001, "套餐不存在或已下架")

        # 创建订单
        order = Order(
            order_no=self._generate_order_no(),
            user_id=user.id,
            package_id=package_id,
            amount=package.price,
            points=package.points,
            status=OrderStatus.PENDING,
        )
        self.db.add(order)
        await self.db.flush()

        logger.info(f"[PointService] 创建充值订单: order_no={order.order_no}")
        return order

    async def get_packages(self) -> List[Package]:
        """获取所有可用套餐"""
        result = await self.db.execute(
            select(Package)
            .where(Package.status == "1")
            .order_by(Package.sort_order, Package.price)
        )
        return list(result.scalars().all())

    async def complete_order(
        self, order_no: str, pay_channel: str = "mock"
    ) -> Order:
        """
        完成订单支付（模拟）
        实际生产中应该由支付回调触发
        """
        # 获取订单
        result = await self.db.execute(
            select(Order).where(Order.order_no == order_no)
        )
        order = result.scalar_one_or_none()
        if not order:
            raise BusinessException(*ErrorCode.ORDER_NOT_FOUND)

        if order.is_paid:
            raise BusinessException(*ErrorCode.ORDER_PAID)

        # 获取用户
        user_result = await self.db.execute(
            select(User).where(User.id == order.user_id)
        )
        user = user_result.scalar_one_or_none()
        if not user:
            raise BusinessException(*ErrorCode.USER_NOT_FOUND)

        # 获取套餐
        package_result = await self.db.execute(
            select(Package).where(Package.id == order.package_id)
        )
        package = package_result.scalar_one_or_none()

        # 更新订单状态
        order.status = OrderStatus.PAID
        order.pay_channel = pay_channel
        order.paid_at = datetime.utcnow()

        # 充值积分
        total_points = order.points + (package.bonus_points if package else 0)
        await self.recharge(
            user, total_points, f"订单充值: {order.order_no}", order.order_no
        )

        await self.db.commit()
        logger.info(f"[PointService] 完成订单支付: order_no={order_no}")
        return order

    async def get_order(self, order_no: str) -> Optional[Order]:
        """获取订单详情"""
        result = await self.db.execute(
            select(Order).where(Order.order_no == order_no)
        )
        return result.scalar_one_or_none()
