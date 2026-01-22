"""
ACM算法学习平台 - SQLite异步连接配置
使用SQLAlchemy 2.0配置SQLite异步连接
适用于开发环境
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


async def init_sqlite():
    """初始化SQLite连接"""
    global engine, async_session_factory

    import os
    # 获取backend目录
    # __file__ 位于 backend/app/infrastructure/database/sqlite.py
    # 需要向上4级到达backend目录
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
    db_path = os.path.join(backend_dir, 'acm_platform.db')

    # 使用绝对路径
    sqlite_url = f"sqlite+aiosqlite:///{db_path}"

    logger.info(f"正在连接SQLite: {sqlite_url}")

    _engine = create_async_engine(
        sqlite_url,
        echo=settings.app_debug,
        # SQLite不需要连接池
    )

    _async_session_factory = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    # 更新全局变量
    engine = _engine
    async_session_factory = _async_session_factory

    logger.info(f"SQLite连接初始化成功: {db_path}")


async def close_sqlite():
    """关闭SQLite连接"""
    global engine

    if engine:
        await engine.dispose()
        logger.info("SQLite连接已关闭")


async def get_sqlite_session() -> AsyncSession:
    """获取SQLite会话（依赖注入用）

    Note: 返回会话对象，调用方需要显式调用 commit() 和 close()
    """
    return async_session_factory()
