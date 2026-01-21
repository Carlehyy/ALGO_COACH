"""
AI Coach API端点
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Body
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.mysql import get_mysql_session
from app.api.deps import get_current_user
from app.services.coach_service import CoachService
from app.core.response import Response
from loguru import logger

router = APIRouter(prefix="/coach", tags=["AI教练"])


@router.post("/sessions", response_model=Response)
async def create_session(
    title: str = Body("新对话"),
    topic_id: str = Body(None),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """创建对话会话"""
    service = CoachService(db)
    session = await service.create_session(current_user, title, topic_id)
    return Response.success(data={"id": str(session.id), "title": session.title})


@router.get("/sessions", response_model=Response)
async def get_sessions(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """获取会话列表"""
    service = CoachService(db)
    sessions = await service.get_sessions(current_user)
    return Response.success(data=[{
        "id": str(s.id),
        "title": s.title,
        "message_count": s.message_count,
        "total_tokens": s.total_tokens,
        "created_at": s.created_at.isoformat(),
        "updated_at": s.updated_at.isoformat(),
    } for s in sessions])


@router.get("/sessions/{session_id}", response_model=Response)
async def get_session(
    session_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """获取会话详情"""
    service = CoachService(db)
    session = await service.get_session(session_id)
    if not session:
        return Response.fail(code=50004, message="会话不存在")
    return Response.success(data={
        "id": str(session.id),
        "title": session.title,
        "topic_id": session.topic_id,
        "message_count": session.message_count,
        "total_tokens": session.total_tokens,
        "status": session.status,
    })


@router.get("/sessions/{session_id}/messages", response_model=Response)
async def get_messages(
    session_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """获取历史消息"""
    service = CoachService(db)
    messages = await service.get_messages(session_id)
    return Response.success(data=[{
        "role": msg.role,
        "content": msg.content,
        "tokens": msg.tokens,
        "created_at": msg.created_at.isoformat(),
    } for msg in messages])


@router.post("/chat", response_model=Response)
async def chat(
    session_id: str = Body(..., embed=True),
    message: str = Body(..., embed=True),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """发送消息（非流式，用于测试）"""
    service = CoachService(db)
    result = await service.chat(current_user, session_id, message)
    return Response.success(data=result)


@router.post("/chat/stream")
async def chat_stream(
    session_id: str = Body(..., embed=True),
    message: str = Body(..., embed=True),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """发送消息（SSE流式响应）"""
    service = CoachService(db)

    async def generate():
        async for chunk in service.chat_stream_generator(current_user, session_id, message):
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@router.delete("/sessions/{session_id}", response_model=Response)
async def close_session(
    session_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """关闭会话"""
    service = CoachService(db)
    await service.close_session(session_id)
    return Response.success(message="会话已关闭")
