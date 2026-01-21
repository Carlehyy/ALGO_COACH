"""
ACM算法学习平台 - MongoDB异步连接配置
使用Motor/Beanie配置MongoDB连接
参考：开发指南V3 - 6.7 数据库连接
"""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from loguru import logger

from app.config import settings

# MongoDB客户端
mongo_client: AsyncIOMotorClient = None


async def init_mongo():
    """初始化MongoDB连接"""
    global mongo_client

    logger.info(f"正在连接MongoDB: {settings.mongodb_host}:{settings.mongodb_port}/{settings.mongodb_database}")

    # 创建Motor客户端
    mongo_client = AsyncIOMotorClient(settings.mongodb_url)

    # 测试连接
    await mongo_client.admin.command('ping')

    logger.info("MongoDB连接初始化成功")

    # TODO: 在添加文档模型后，需要初始化Beanie
    # await init_beanie(
    #     database=mongo_client[settings.mongodb_database],
    #     document_models=[
    #         # 在这里添加所有Beanie文档模型
    #         # app.models.mongo.note.Note,
    #         # app.models.mongo.chat.ChatSession,
    #     ]
    # )


async def close_mongo():
    """关闭MongoDB连接"""
    global mongo_client

    if mongo_client:
        mongo_client.close()
        logger.info("MongoDB连接已关闭")


def get_mongo_database():
    """获取MongoDB数据库实例"""
    return mongo_client[settings.mongodb_database]
