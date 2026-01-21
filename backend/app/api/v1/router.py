"""
ACM算法学习平台 - API路由汇总
参考：开发指南V3 - 6.11 路由注册
"""

from fastapi import APIRouter

# 导入各模块路由
from app.api.v1.endpoints import user, topic, note, point, coach, resource, admin
# from app.api.v1.endpoints import resource, admin

# 创建API路由
api_router = APIRouter()

# 注册各模块路由
api_router.include_router(user.router, tags=["用户管理"])
api_router.include_router(topic.router, tags=["知识点管理"])
api_router.include_router(note.router, tags=["笔记管理"])
api_router.include_router(point.router, tags=["积分管理"])
api_router.include_router(coach.router, tags=["AI教练"])
api_router.include_router(resource.router, tags=["资源管理"])
api_router.include_router(admin.router, tags=["管理后台"])


@api_router.get("/")
async def api_root():
    """API根路径"""
    return {
        "message": "ACM Learning Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }
