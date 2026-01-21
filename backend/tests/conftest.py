"""
Pytest测试配置和Fixtures
参考：开发指南V3 - 9.2 pytest配置
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from unittest.mock import AsyncMock

from app.infrastructure.database.mysql import Base
from app.config import settings


# 测试数据库引擎
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
async def test_engine():
    """测试数据库引擎"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """测试数据库会话"""
    async_session_maker = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture
def mock_redis():
    """Mock Redis客户端"""
    return AsyncMock()


@pytest.fixture
def mock_mongo():
    """Mock MongoDB客户端"""
    return AsyncMock()


@pytest.fixture
def mock_minio():
    """Mock MinIO客户端"""
    return AsyncMock()


@pytest.fixture
def mock_ai_client():
    """Mock AI客户端"""
    return AsyncMock()


@pytest.fixture
async def mock_current_user():
    """Mock当前登录用户"""
    user = AsyncMock()
    user.id = 1
    user.email = "test@example.com"
    user.nickname = "Test User"
    user.points = 100
    user.role = "user"
    user.status = 1
    return user


@pytest.fixture
def override_dependencies(db_session, mock_redis, mock_mongo, mock_minio):
    """覆盖依赖注入"""
    from app.infrastructure.database.mysql import get_mysql_session
    from app.infrastructure.cache.redis import get_redis
    from app.api.deps import get_current_user

    async def override_get_mysql_session():
        yield db_session

    async def override_get_redis():
        return mock_redis

    async def override_get_current_user():
        return await mock_current_user()

    # 在实际使用时需要使用 app.dependency_overrides
    # 这里只是定义了override函数
    yield {
        "get_mysql_session": override_get_mysql_session,
        "get_redis": override_get_redis,
        "get_current_user": override_get_current_user,
    }
