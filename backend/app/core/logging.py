"""
ACM算法学习平台 - 日志配置
使用Loguru配置日志系统
参考：开发指南V3 - 10.1 日志配置
"""

import sys
from loguru import logger
from app.config import settings


def setup_logging():
    """配置日志系统"""

    # 移除默认的handler
    logger.remove()

    # 控制台输出 - 彩色格式
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # 应用日志文件 - 按天轮转
    logger.add(
        settings.log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        rotation="00:00",  # 每天午夜轮转
        retention="30 days",  # 保留30天
        compression="zip",  # 压缩旧日志
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
    )

    # 错误日志文件 - 单独记录
    logger.add(
        settings.error_log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="00:00",
        retention="60 days",  # 错误日志保留60天
        compression="zip",
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
    )

    logger.info("日志系统初始化完成")
    logger.info(f"日志级别: {settings.log_level}")
    logger.info(f"应用日志: {settings.log_file}")
    logger.info(f"错误日志: {settings.error_log_file}")


# 自动配置日志
setup_logging()


# 导出logger实例
__all__ = ["logger"]
