"""
ACM算法学习平台 - MySQL异步连接配置
使用SQLAlchemy 2.0配置MySQL异步连接池
参考：开发指南V3 - 6.7 数据库连接
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from loguru import logger

from app.config import settings


# SQLAlchemy Base
class Base(DeclarativeBase):
    """SQLAlchemy基类"""
    pass


# 创建异步引擎
engine = None
async_session_factory = None


async def init_mysql():
    """初始化MySQL连接"""
    global engine, async_session_factory

    logger.info(f"正在连接MySQL: {settings.mysql_host}:{settings.mysql_port}/{settings.mysql_database}")

    engine = create_async_engine(
        settings.mysql_url,
        echo=settings.app_debug,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

    async_session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    logger.info("MySQL连接池初始化成功")


async def close_mysql():
    """关闭MySQL连接"""
    global engine

    if engine:
        await engine.dispose()
        logger.info("MySQL连接已关闭")


async def get_mysql_session() -> AsyncSession:
    """获取MySQL会话（依赖注入用）"""
    async with async_session_factory() as session:
        yield session
