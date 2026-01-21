"""
ACM算法学习平台 - 统一响应格式
参考：开发指南V3 - 6.4 统一响应格式
"""

from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel
from datetime import datetime

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    """统一响应格式"""

    code: int = 200
    message: str = "success"
    data: Optional[T] = None
    timestamp: int = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.timestamp is None:
            self.timestamp = int(datetime.now().timestamp() * 1000)

    @classmethod
    def success(cls, data: Any = None, message: str = "success") -> "Response":
        """成功响应"""
        return cls(code=200, message=message, data=data)

    @classmethod
    def fail(cls, code: int = 400, message: str = "error", data: Any = None) -> "Response":
        """失败响应"""
        return cls(code=code, message=message, data=data)


class PageData(BaseModel, Generic[T]):
    """分页数据"""

    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    def __init__(self, **data):
        super().__init__(**data)
        if self.total_pages == 0:
            self.total_pages = (self.total + self.page_size - 1) // self.page_size


class PageResponse(BaseModel, Generic[T]):
    """分页响应"""

    code: int = 200
    message: str = "success"
    data: PageData[T]
    timestamp: int = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.timestamp is None:
            self.timestamp = int(datetime.now().timestamp() * 1000)

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        page: int = 1,
        page_size: int = 20,
        message: str = "success",
    ) -> "PageResponse":
        """创建分页响应"""
        page_data = PageData(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
        )
        return cls(code=200, message=message, data=page_data)
