"""
ACM算法学习平台 - 依赖注入模块
参考：开发指南V3 - 6.11 依赖注入
"""

from typing import Optional
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.mysql import get_mysql_session
from app.core.security import decode_token
from app.core.exceptions import BusinessException, ErrorCode


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_mysql_session),
):
    """
    获取当前登录用户
    通过Authorization头获取Token并解析用户信息
    """
    if not authorization:
        raise BusinessException(*ErrorCode.UNAUTHORIZED)

    # Bearer Token格式
    if not authorization.startswith("Bearer "):
        raise BusinessException(*ErrorCode.TOKEN_INVALID)

    token = authorization.replace("Bearer ", "")
    user_id = decode_token(token)

    if not user_id:
        raise BusinessException(*ErrorCode.TOKEN_EXPIRED)

    # 从数据库获取用户
    # TODO: 实现 UserRepository 并获取用户
    # user = await user_repo.get_by_id(db, int(user_id))
    # if not user:
    #     raise BusinessException(*ErrorCode.USER_NOT_FOUND)

    # 临时返回模拟用户
    return {"id": user_id, "email": "temp@example.com"}


async def get_current_admin(current_user = Depends(get_current_user)):
    """
    获取管理员用户
    验证当前用户是否为管理员
    """
    if current_user.get("role") != "admin":
        raise BusinessException(*ErrorCode.FORBIDDEN)
    return current_user


async def get_optional_user(
    authorization: Optional[str] = Header(None),
):
    """
    获取可选用户
    允许未登录用户访问，如果有Token则解析
    """
    if not authorization:
        return None

    if not authorization.startswith("Bearer "):
        return None

    token = authorization.replace("Bearer ", "")
    user_id = decode_token(token)

    if not user_id:
        return None

    return {"id": user_id}


async def require_auth(
    current_user = Depends(get_current_user),
):
    """
    要求认证的依赖
    用于需要登录才能访问的接口
    """
    return current_user
