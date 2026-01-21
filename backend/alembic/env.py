"""
Alembic环境配置
参考：开发指南V3 - 6.7 数据库连接
"""

import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 导入配置和模型
from app.config import settings
from app.infrastructure.database.mysql import Base

# 导入所有模型（用于自动生成迁移）
# from app.models.mysql import user, topic, point, order, resource, note

# Alembic配置对象
config = context.config

# 设置数据库连接URL
config.set_main_option("sqlalchemy.url", settings.mysql_url.replace("+aiomysql", "+pymysql"))

# 解析日志配置
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 目标元数据
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """离线模式运行迁移"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """执行迁移"""
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """异步运行迁移"""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.mysql_url.replace("+aiomysql", "+pymysql")

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """在线模式运行迁移"""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
