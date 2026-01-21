"""
ACM算法学习平台 - Redis客户端配置
参考：开发指南V3 - 6.7 数据库连接
"""

import redis.asyncio as aioredis
from loguru import logger

from app.config import settings

# Redis客户端
redis_client: aioredis.Redis = None


async def init_redis():
    """初始化Redis连接"""
    global redis_client

    logger.info(f"正在连接Redis: {settings.redis_host}:{settings.redis_port}/{settings.redis_db}")

    redis_client = await aioredis.from_url(
        settings.redis_url,
        db=settings.redis_db,
        encoding="utf-8",
        decode_responses=True,
    )

    # 测试连接
    await redis_client.ping()

    logger.info("Redis连接初始化成功")


async def close_redis():
    """关闭Redis连接"""
    global redis_client

    if redis_client:
        await redis_client.close()
        logger.info("Redis连接已关闭")


def get_redis() -> aioredis.Redis:
    """获取Redis客户端实例"""
    return redis_client
