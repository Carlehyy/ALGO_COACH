"""
ACM算法学习平台 - 用户相关的Pydantic模式
参考：开发指南V3 - 6.10 API端点示例
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


# ============ 请求模式 ============

class UserCreate(BaseModel):
    """用户注册请求"""
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., min_length=6, max_length=50, description="密码(6-50字符)")
    nickname: Optional[str] = Field(None, max_length=100, description="昵称")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "user@example.com",
            "password": "password123",
            "nickname": "用户昵称"
        }
    })


class UserLogin(BaseModel):
    """用户登录请求"""
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., description="密码")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "user@example.com",
            "password": "password123"
        }
    })


class UserUpdate(BaseModel):
    """用户更新请求"""
    nickname: Optional[str] = Field(None, max_length=100, description="昵称")
    avatar: Optional[str] = Field(None, max_length=500, description="头像URL")
    leetcode_username: Optional[str] = Field(None, max_length=100, description="LeetCode用户名")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "nickname": "新昵称",
            "avatar": "https://example.com/avatar.jpg",
            "leetcode_username": "leetcode_user"
        }
    })


class ChangePassword(BaseModel):
    """修改密码请求"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, max_length=50, description="新密码(6-50字符)")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "old_password": "old_password123",
            "new_password": "new_password123"
        }
    })


# ============ 响应模式 ============

class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    email: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    points: int = 0
    total_recharged: int = 0
    total_consumed: int = 0
    leetcode_username: Optional[str] = None
    ability_score: int = 0
    status: str = "1"
    role: str = "user"
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": 1,
            "email": "user@example.com",
            "nickname": "用户昵称",
            "avatar": "https://example.com/avatar.jpg",
            "points": 100,
            "total_recharged": 0,
            "total_consumed": 0,
            "leetcode_username": "leetcode_user",
            "ability_score": 50,
            "status": "1",
            "role": "user",
            "created_at": "2026-01-20T00:00:00",
            "updated_at": "2026-01-20T00:00:00",
            "last_login_at": "2026-01-20T12:00:00"
        }
    })


class TokenResponse(BaseModel):
    """Token响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "user": {
                "id": 1,
                "email": "user@example.com",
                "nickname": "用户昵称"
            }
        }
    })


class RefreshTokenRequest(BaseModel):
    """刷新Token请求"""
    refresh_token: str = Field(..., description="刷新令牌")


# ============ 内部使用模式 ============

class UserInDB(UserResponse):
    """数据库中的用户信息（包含密码哈希）"""
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
