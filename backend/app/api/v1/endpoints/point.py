"""
积分API端点
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.mysql import get_mysql_session
from app.api.deps import get_current_user
from app.services.point_service import PointService
from app.core.response import Response, PageResponse
from loguru import logger

router = APIRouter(prefix="/points", tags=["积分管理"])


@router.get("/balance", response_model=Response)
async def get_balance(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """查询积分余额"""
    service = PointService(db)
    balance = await service.get_balance(current_user)
    return Response.success(data=balance)


@router.get("/logs", response_model=PageResponse)
async def get_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """获取积分流水"""
    service = PointService(db)
    skip = (page - 1) * page_size
    logs, total = await service.get_logs(current_user, skip, page_size)
    log_dicts = [log.to_dict() for log in logs]
    return PageResponse.create(items=log_dicts, total=total, page=page, page_size=page_size)


@router.get("/packages", response_model=Response)
async def get_packages(
    db: AsyncSession = Depends(get_mysql_session),
):
    """获取积分套餐列表"""
    service = PointService(db)
    packages = await service.get_packages()
    return Response.success(data=[p.to_dict() for p in packages])


@router.post("/orders", response_model=Response)
async def create_order(
    package_id: int = Body(..., embed=True),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """创建充值订单"""
    service = PointService(db)
    order = await service.create_order(current_user, package_id)
    return Response.success(data=order.to_dict())


@router.post("/orders/{order_no}/callback", response_model=Response)
async def order_callback(
    order_no: str,
    pay_channel: Optional[str] = Body("mock", embed=True),
    db: AsyncSession = Depends(get_mysql_session),
):
    """
    支付回调（模拟）
    实际生产中应该由第三方支付平台回调
    """
    service = PointService(db)
    order = await service.complete_order(order_no, pay_channel)
    return Response.success(data=order.to_dict(), message="支付成功")


@router.get("/orders/{order_no}", response_model=Response)
async def get_order(
    order_no: str,
    db: AsyncSession = Depends(get_mysql_session),
):
    """查询订单状态"""
    service = PointService(db)
    order = await service.get_order(order_no)
    if not order:
        return Response.fail(code=40003, message="订单不存在")
    return Response.success(data=order.to_dict())
