"""
AI Coach业务逻辑层
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks

from app.models.mongo.chat import ChatSession, ChatMessage
from app.models.mysql.user import User
from app.infrastructure.ai.claude_client import get_mock_claude_client
from app.services.point_service import PointService
from app.core.exceptions import BusinessException, ErrorCode
from loguru import logger


class CoachService:
    """AI教练业务逻辑类"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.claude_client = get_mock_claude_client()
        self.point_service = PointService(db)

    async def create_session(
        self, user: User, title: str = "新对话", topic_id: Optional[str] = None
    ) -> ChatSession:
        """创建聊天会话"""
        session = ChatSession(
            user_id=user.id,
            title=title,
            topic_id=topic_id,
        )
        await session.save()
        logger.info(f"[CoachService] 创建会话: id={session.id}, user_id={user.id}")
        return session

    async def get_sessions(self, user: User) -> List[ChatSession]:
        """获取用户的会话列表"""
        sessions = await ChatSession.find(
            ChatSession.user_id == user.id,
            ChatSession.status == "active"
        ).sort(-ChatSession.updated_at).to_list()
        return sessions

    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        """获取会话详情"""
        return await ChatSession.get(session_id)

    async def close_session(self, session_id: str) -> None:
        """关闭会话"""
        session = await self.get_session(session_id)
        if session:
            session.status = "closed"
            session.updated_at = datetime.utcnow()
            await session.save()
            logger.info(f"[CoachService] 关闭会话: id={session_id}")

    async def get_messages(self, session_id: str) -> List[ChatMessage]:
        """获取会话的历史消息"""
        messages = await ChatMessage.find(
            {"session_id": session_id}
        ).sort(ChatMessage.created_at).to_list()
        return messages

    async def chat(
        self,
        user: User,
        session_id: str,
        user_message: str,
        background_tasks: BackgroundTasks = None,
    ) -> dict:
        """
        发送消息（流式响应的包装）
        返回AI回复和元数据
        """
        # 获取会话
        session = await self.get_session(session_id)
        if not session:
            raise BusinessException(*ErrorCode.SESSION_NOT_FOUND)
        if session.status != "active":
            raise BusinessException(*ErrorCode.SESSION_CLOSED)

        # 检查积分（每次对话消耗10积分）
        COACH_POINTS_PER_MESSAGE = 10
        if not await self.point_service.check_balance(user, COACH_POINTS_PER_MESSAGE):
            raise BusinessException(*ErrorCode.POINTS_NOT_ENOUGH)

        # 获取历史消息
        history = await self.get_messages(session_id)
        messages = [{"role": msg.role, "content": msg.content} for msg in history]
        messages.append({"role": "user", "content": user_message})

        # 保存用户消息
        user_msg = ChatMessage(
            session_id=session.id,
            role="user",
            content=user_message,
            tokens=len(user_message) // 4,
        )
        await user_msg.save()

        # 调用AI（非流式，用于获取完整回复）
        result = await self.claude_client.chat(messages)

        # 保存AI回复
        assistant_msg = ChatMessage(
            session_id=session.id,
            role="assistant",
            content=result["content"],
            tokens=result.get("output_tokens", 0),
        )
        await assistant_msg.save()

        # 更新会话
        session.message_count += 2
        session.total_tokens += result.get("input_tokens", 0) + result.get("output_tokens", 0)
        session.updated_at = datetime.utcnow()

        # 更新标题（使用第一条用户消息）
        if session.message_count == 2:
            session.title = user_message[:30] + "..." if len(user_message) > 30 else user_message

        await session.save()

        # 扣除积分
        await self.point_service.consume(
            user, COACH_POINTS_PER_MESSAGE, "AI对话消费", str(session.id)
        )
        await self.db.commit()

        logger.info(
            f"[CoachService] AI对话: session_id={session_id}, tokens={result.get('output_tokens', 0)}"
        )

        return {
            "content": result["content"],
            "tokens": result.get("output_tokens", 0),
            "session_id": str(session.id),
        }

    async def chat_stream_generator(
        self, user: User, session_id: str, user_message: str
    ):
        """
        流式对话生成器（用于SSE）
        返回流式文本块
        """
        # 获取会话
        session = await self.get_session(session_id)
        if not session:
            yield f"data: {json.dumps({'error': '会话不存在'})}\n\n"
            return

        # 检查积分
        COACH_POINTS_PER_MESSAGE = 10
        try:
            if not await self.point_service.check_balance(user, COACH_POINTS_PER_MESSAGE):
                yield f"data: {json.dumps({'error': '积分不足'})}\n\n"
                return
        except:
            yield f"data: {json.dumps({'error': '积分检查失败'})}\n\n"
            return

        # 获取历史消息
        history = await self.get_messages(session_id)
        messages = [{"role": msg.role, "content": msg.content} for msg in history]
        messages.append({"role": "user", "content": user_message})

        # 保存用户消息
        user_msg = ChatMessage(
            session_id=session.id,
            role="user",
            content=user_message,
            tokens=len(user_message) // 4,
        )
        await user_msg.save()

        # 流式生成AI回复
        full_response = ""
        async for chunk in self.claude_client.chat_stream(messages):
            full_response += chunk
            # 发送SSE格式的数据
            yield f"data: {json.dumps({'content': chunk, 'done': False})}\n\n"

        # 发送结束标记
        yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"

        # 保存完整回复
        assistant_msg = ChatMessage(
            session_id=session.id,
            role="assistant",
            content=full_response,
            tokens=len(full_response) // 4,
        )
        await assistant_msg.save()

        # 更新会话
        session.message_count += 2
        session.total_tokens += len(user_message) // 4 + len(full_response) // 4
        session.updated_at = datetime.utcnow()
        if session.message_count == 2:
            session.title = user_message[:30] + "..." if len(user_message) > 30 else user_message
        await session.save()

        # 扣除积分
        await self.point_service.consume(
            user, COACH_POINTS_PER_MESSAGE, "AI对话消费", str(session.id)
        )
        await self.db.commit()

        logger.info(f"[CoachService] 流式对话完成: session_id={session_id}")


# 导入json用于SSE
import json
