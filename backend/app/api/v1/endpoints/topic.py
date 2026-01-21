"""
Topic API端点
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.mysql import get_mysql_session
from app.services.topic_service import TopicService
from app.core.response import Response

router = APIRouter(prefix="/topics", tags=["知识点管理"])


@router.get("/", response_model=Response)
async def get_topics(
    db: AsyncSession = Depends(get_mysql_session),
):
    """获取知识点列表/树"""
    service = TopicService(db)
    tree = await service.get_topic_tree()
    return Response.success(data=tree)


@router.get("/categories", response_model=Response)
async def get_categories():
    """获取所有分类"""
    categories = {
        "basic": "基础算法",
        "data_structure": "数据结构",
        "dp": "动态规划",
        "graph": "图论",
        "string": "字符串",
        "math": "数学",
    }
    return Response.success(data=categories)


@router.get("/{topic_id}", response_model=Response)
async def get_topic_detail(
    topic_id: str,
    db: AsyncSession = Depends(get_mysql_session),
):
    """获取知识点详情"""
    service = TopicService(db)
    detail = await service.get_topic_detail(topic_id)
    if not detail:
        return Response.fail(code=10004, message="知识点不存在")
    return Response.success(data=detail)


@router.get("/{topic_id}/prerequisites", response_model=Response)
async def get_prerequisites(
    topic_id: str,
    db: AsyncSession = Depends(get_mysql_session),
):
    """获取前置知识点"""
    service = TopicService(db)
    prerequisites = await service.topic_repo.get_prerequisites(topic_id)
    return Response.success(data=[p.to_dict() for p in prerequisites])


@router.get("/{topic_id}/related", response_model=Response)
async def get_related(
    topic_id: str,
    db: AsyncSession = Depends(get_mysql_session),
):
    """获取相关知识点"""
    service = TopicService(db)
    related = await service.topic_repo.get_related(topic_id)
    return Response.success(data=[r.to_dict() for p in related])
