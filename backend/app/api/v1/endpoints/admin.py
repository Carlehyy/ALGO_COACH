"""
Admin API端点 - 管理后台
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.mysql import get_mysql_session
from app.api.deps import get_current_admin
from app.services.resource_service import ResourceService
from app.core.response import Response, PageResponse
from loguru import logger

router = APIRouter(prefix="/admin", tags=["管理后台"])


@router.get("/dashboard", response_model=Response)
async def get_dashboard(
    db: AsyncSession = Depends(get_mysql_session),
):
    """管理后台 - 数据统计"""
    # TODO: 实际统计数据
    stats = {
        "users_count": 0,
        "notes_count": 0,
        "resources_count": 0,
        "today_revenue": 0,
        "week_revenue": 0,
        "month_revenue": 0,
        "pending_reviews": 0,
    }

    # TODO: 查询数据库获取真实统计
    # from sqlalchemy import func, select
    # from app.models.mysql import user, resource

    return Response.success(data=stats)


@router.get("/resources", response_model=PageResponse)
async def get_admin_resources(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    current_admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_mysql_session),
):
    """管理后台 - 资源列表"""
    service = ResourceService(db)
    skip = (page - 1) * page_size
    resources, total = await service.get_resources(
        skip, page_size, type, status, status
    )
    resource_dicts = [r.to_dict() for r in resources]
    return PageResponse.create(items=resource_dicts, total=total, page=page, page_size=page_size)


@router.get("/notes/pending", response_model=Response)
async def get_pending_notes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_mysql_session),
):
    """管理后台 - 待审核笔记列表"""
    # TODO: 从MongoDB获取status=1的笔记
    notes = []
    total = 0

    return PageResponse.create(items=notes, total=total, page=page, page_size=page_size)


@router.post("/notes/{note_id}/publish", response_model=Response)
async def publish_note(
    note_id: str,
    current_admin = Depends(get_current_admin),
):
    """管理后台 - 发布笔记"""
    # TODO: 更新MongoDB中笔记状态为已发布
    return Response.success(message="笔记已发布")


@router.post("/notes/{note_id}/reject", response_model=Response)
async def reject_note(
    note_id: str,
    reason: str = Body(..., description="拒绝原因"),
    current_admin = Depends(get_current_admin),
):
    """管理后台 - 退回笔记"""
    # TODO: 更新MongoDB中笔记状态为草稿
    return Response.success(message="笔记已退回")


@router.get("/users", response_model=PageResponse)
async def get_admin_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    current_admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_mysql_session),
):
    """管理后台 - 用户列表"""
    from app.models.mysql.user import User
    from sqlalchemy import select

    query = select(User)
    if status:
        query = query.where(User.status == status)

    count_result = await db.execute(select(User.id))
    total = len(count_result.all())

    skip = (page - 1) * page_size
    query = query.offset(skip).limit(page_size).order_by(User.id.desc())
    result = await db.execute(query)
    users = result.scalars().all()

    user_dicts = [u.to_dict() for u in users]
    return PageResponse.create(items=user_dicts, total=total, page=page, page_size=page_size)


@router.put("/users/{user_id}/status", response_model=Response)
async def update_user_status(
    user_id: int,
    status: str = Body(..., description="状态(0禁用 1正常)"),
    current_admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_mysql_session),
):
    """管理后台 - 更新用户状态"""
    from app.models.mysql.user import User
    from sqlalchemy import select

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return Response.fail(code=20001, message="用户不存在")

    user.status = status
    await db.commit()

    logger.info(f"[Admin] 用户状态更新: user_id={user_id}, status={status}")
    return Response.success(message="用户状态已更新")


@router.post("/notes/{note_id}/generate", response_model=Response)
async def generate_note(
    note_id: str,
    current_admin = Depends(get_current_admin),
):
    """管理后台 - 触发笔记生成任务"""
    # TODO: 创建Celery异步任务生成笔记
    return Response.success(message="笔记生成任务已触发")
