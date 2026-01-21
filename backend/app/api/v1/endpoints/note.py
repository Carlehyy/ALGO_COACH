"""
Note API端点
"""

from fastapi import APIRouter, Query

from app.services.note_service import NoteService
from app.core.response import Response, PageResponse
from loguru import logger

router = APIRouter(prefix="/notes", tags=["笔记管理"])


@router.get("/", response_model=Response)
async def get_notes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    topic_id: str = Query(None),
    keyword: str = Query(None),
):
    """获取笔记列表（分页）"""
    service = NoteService()

    if topic_id:
        # 按知识点查询
        notes = await service.get_notes_by_topic(topic_id)
        return Response.success(data=[n.dict() for n in notes])
    elif keyword:
        # 搜索
        notes = await service.search_notes(keyword, page_size)
        return Response.success(data=[n.dict() for n in notes])
    else:
        # 分页获取
        notes, total = await service.get_published_notes(page, page_size)
        note_dicts = [n.dict() for n in notes]
        return PageResponse.create(
            items=note_dicts,
            total=total,
            page=page,
            page_size=page_size,
        )


@router.get("/{note_id}", response_model=Response)
async def get_note_detail(note_id: str):
    """获取笔记详情"""
    service = NoteService()
    note = await service.get_note(note_id)
    if not note:
        return Response.fail(code=30001, message="笔记不存在")
    return Response.success(data=note.dict())


@router.get("/topic/{topic_id}", response_model=Response)
async def get_notes_by_topic(topic_id: str):
    """根据知识点获取笔记"""
    service = NoteService()
    notes = await service.get_notes_by_topic(topic_id)
    return Response.success(data=[n.dict() for n in notes])
