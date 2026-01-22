"""
初始化SQLite数据库并创建表
"""

import asyncio
from app.infrastructure.database.sqlite import init_sqlite


async def create_tables():
    """创建数据库表"""
    await init_sqlite()

    # 在初始化后再导入engine
    from app.infrastructure.database.sqlite import engine

    async with engine.begin() as conn:
        # 导入所有模型以确保它们被注册到 Base.metadata
        from app.models.mysql import user

        # 创建所有表
        from app.infrastructure.database.sqlite import Base
        await conn.run_sync(Base.metadata.create_all)

        print("✅ 数据库表创建成功")


if __name__ == "__main__":
    asyncio.run(create_tables())
