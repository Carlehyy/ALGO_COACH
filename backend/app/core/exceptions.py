"""
ACM算法学习平台 - 全局异常处理
参考：开发指南V3 - 6.5 异常处理
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger


class BusinessException(Exception):
    """业务异常基类"""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class ErrorCode:
    """错误码定义"""

    # === 通用错误 1xxxx ===
    PARAM_ERROR = (10001, "参数错误")
    UNAUTHORIZED = (10002, "未授权，请先登录")
    FORBIDDEN = (10003, "无权限访问")
    NOT_FOUND = (10004, "资源不存在")
    SERVER_ERROR = (10005, "服务器内部错误")
    RATE_LIMIT = (10006, "请求过于频繁")

    # === 用户错误 2xxxx ===
    USER_NOT_FOUND = (20001, "用户不存在")
    USER_EXISTS = (20002, "用户已存在")
    PASSWORD_ERROR = (20003, "密码错误")
    USER_DISABLED = (20004, "用户已被禁用")
    TOKEN_INVALID = (20005, "Token无效或已过期")
    TOKEN_EXPIRED = (20006, "Token已过期")

    # === 笔记错误 3xxxx ===
    NOTE_NOT_FOUND = (30001, "笔记不存在")
    NOTE_NOT_PUBLISHED = (30002, "笔记未发布")
    NOTE_ALREADY_EXISTS = (30003, "笔记已存在")

    # === 积分错误 4xxxx ===
    POINTS_NOT_ENOUGH = (40001, "积分不足")
    POINTS_CONSUME_FAILED = (40002, "积分扣减失败")
    ORDER_NOT_FOUND = (40003, "订单不存在")
    ORDER_PAID = (40004, "订单已支付")

    # === AI错误 5xxxx ===
    AI_CALL_FAILED = (50001, "AI调用失败")
    AI_QUOTA_EXCEEDED = (50002, "AI调用次数超限")
    AI_TIMEOUT = (50003, "AI调用超时")
    SESSION_NOT_FOUND = (50004, "会话不存在")
    SESSION_CLOSED = (50005, "会话已关闭")

    # === 资源错误 6xxxx ===
    RESOURCE_NOT_FOUND = (60001, "资源不存在")
    RESOURCE_UPLOAD_FAILED = (60002, "资源上传失败")
    RESOURCE_TYPE_NOT_ALLOWED = (60003, "不支持的资源类型")
    FILE_TOO_LARGE = (60004, "文件过大")

    # === 知识点错误 7xxxx ===
    TOPIC_NOT_FOUND = (70001, "知识点不存在")
    PREREQUISITES_NOT_MET = (70002, "未满足前置条件")


def setup_exception_handlers(app: FastAPI):
    """设置全局异常处理器"""

    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        """业务异常处理"""
        logger.warning(f"[BUSINESS_ERROR] {exc.code}: {exc.message}")
        return JSONResponse(
            status_code=200,
            content={"code": exc.code, "message": exc.message, "data": None},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """值错误处理"""
        logger.warning(f"[VALUE_ERROR] {str(exc)}")
        return JSONResponse(
            status_code=200,
            content={"code": ErrorCode.PARAM_ERROR[0], "message": str(exc), "data": None},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """通用异常处理"""
        logger.error(f"[SERVER_ERROR] {type(exc).__name__}: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"code": ErrorCode.SERVER_ERROR[0], "message": "服务器内部错误", "data": None},
        )
