"""
ACM算法学习平台 - FastAPI应用入口
参考：开发指南V3 - 6.3 FastAPI应用入口
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config import settings
from app.core.response import Response
from app.core.exceptions import setup_exception_handlers
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info(f"🚀 {settings.app_name} 启动中...")
    logger.info(f"📦 环境: {settings.app_env}")
    logger.info(f"🔧 调试模式: {settings.app_debug}")

    # TODO: 初始化数据库连接
    # TODO: 初始化Redis连接
    # TODO: 初始化MinIO客户端

    yield

    # 关闭时执行
    logger.info("👋 应用关闭中...")
    # TODO: 关闭数据库连接
    # TODO: 关闭Redis连接
    # TODO: 关闭MinIO客户端


def create_app() -> FastAPI:
    """创建FastAPI应用实例"""

    app = FastAPI(
        title=settings.app_name,
        description="AI驱动的个性化算法学习平台",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # 配置CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册全局异常处理器
    setup_exception_handlers(app)

    # 注册路由
    app.include_router(api_router, prefix="/api/v1")

    # 健康检查端点
    @app.get("/health")
    async def health_check():
        """健康检查"""
        return Response.success(data={
            "status": "healthy",
            "app_name": settings.app_name,
            "version": "1.0.0"
        })

    @app.get("/")
    async def root():
        """根路径"""
        return Response.success(data={
            "message": "Welcome to ACM Learning Platform",
            "docs": "/docs",
            "health": "/health"
        })

    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.app_debug,
        log_level=settings.log_level.lower(),
    )
