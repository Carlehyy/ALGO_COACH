"""
ACM算法学习平台 - 用户API端点
参考：开发指南V3 - 6.10 API端点示例
"""

from typing import Optional
from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.mysql import get_mysql_session
from app.api.deps import get_current_user
from app.services.user_service import UserService
from app.api.v1.schemas.user import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    TokenResponse,
    ChangePassword,
)
from app.core.response import Response, PageResponse
from loguru import logger

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.post("/register", response_model=Response[UserResponse])
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_mysql_session),
):
    """
    用户注册

    - **email**: 邮箱地址（必须唯一）
    - **password**: 密码（6-50字符）
    - **nickname**: 昵称（可选）
    """
    service = UserService(db)
    user = await service.create_user(user_in)
    return Response.success(data=UserResponse.model_validate(user))


@router.post("/login", response_model=Response[TokenResponse])
async def login(
    login_in: UserLogin,
    db: AsyncSession = Depends(get_mysql_session),
):
    """
    用户登录

    - **email**: 邮箱地址
    - **password**: 密码

    返回访问令牌和用户信息
    """
    service = UserService(db)
    result = await service.authenticate(login_in.email, login_in.password)
    return Response.success(
        data=TokenResponse(
            access_token=result["access_token"],
            token_type="bearer",
            user=UserResponse.model_validate(result["user"]),
        )
    )


@router.get("/me", response_model=Response[UserResponse])
async def get_me(
    current_user = Depends(get_current_user),
):
    """获取当前登录用户信息"""
    return Response.success(data=UserResponse.model_validate(current_user))


@router.put("/me", response_model=Response[UserResponse])
async def update_me(
    user_in: UserUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """
    更新当前用户信息

    - **nickname**: 昵称（可选）
    - **avatar**: 头像URL（可选）
    - **leetcode_username**: LeetCode用户名（可选）
    """
    service = UserService(db)
    user = await service.update_user(current_user, user_in)
    return Response.success(data=UserResponse.model_validate(user))


@router.post("/change-password", response_model=Response)
async def change_password(
    password_in: ChangePassword,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """
    修改密码

    - **old_password**: 旧密码
    - **new_password**: 新密码（6-50字符）
    """
    service = UserService(db)
    await service.change_password(current_user, password_in.old_password, password_in.new_password)
    return Response.success(message="密码修改成功")


@router.get("/balance", response_model=Response)
async def get_balance(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """获取当前用户积分余额信息"""
    service = UserService(db)
    balance = await service.get_user_balance(current_user)
    return Response.success(data=balance)


@router.post("/refresh", response_model=Response[TokenResponse])
async def refresh_token(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_mysql_session),
):
    """
    刷新访问令牌

    需要在Authorization头中提供有效的refresh_token
    """
    # TODO: 实现刷新令牌逻辑
    # 当前简化为使用现有令牌
    if not authorization:
        return Response.fail(code=10002, message="未提供Token")

    token = authorization.replace("Bearer ", "")
    # 验证并获取用户
    from app.core.security import decode_token
    user_id = decode_token(token)

    if not user_id:
        return Response.fail(code=10006, message="Token无效")

    service = UserService(db)
    user = await service.get_by_id(int(user_id))

    if not user:
        return Response.fail(code=20001, message="用户不存在")

    # 生成新令牌
    from app.core.security import create_access_token
    new_token = create_access_token(str(user.id))

    return Response.success(
        data=TokenResponse(
            access_token=new_token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )
    )


# 管理员接口

@router.get("/", response_model=PageResponse[UserResponse])
async def list_users(
    page: int = 1,
    page_size: int = 20,
    status: Optional[str] = None,
    role: Optional[str] = None,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """
    获取用户列表（管理员）

    - **page**: 页码（从1开始）
    - **page_size**: 每页数量
    - **status**: 状态筛选（0禁用 1正常）
    - **role**: 角色筛选（user/admin）
    """
    # TODO: 添加管理员权限检查
    service = UserService(db)
    users, total = await service.list_users(
        page=page, page_size=page_size, status=status, role=role
    )

    user_responses = [UserResponse.model_validate(u) for u in users]
    return PageResponse.create(items=user_responses, total=total, page=page, page_size=page_size)


@router.post("/{user_id}/disable", response_model=Response)
async def disable_user(
    user_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """
    禁用用户（管理员）

    - **user_id**: 用户ID
    """
    # TODO: 添加管理员权限检查
    service = UserService(db)
    await service.disable_user(user_id)
    return Response.success(message="用户已禁用")
