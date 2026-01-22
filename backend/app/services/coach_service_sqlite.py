"""
ACM算法学习平台 - AI Coach业务逻辑层 (SQLite版本)
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.models.mysql.chat import ChatSession, ChatMessage, ChatSessionStatus
from app.models.mysql.user import User
from app.services.point_service import PointService
from app.core.exceptions import BusinessException, ErrorCode
from app.infrastructure.ai.claude_client import get_mock_claude_client


class CoachService:
    """AI教练业务逻辑类（SQLite版本）"""

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
            topic_id=int(topic_id) if topic_id else None,
        )
        self.db.add(session)
        await self.db.flush()
        await self.db.refresh(session)

        logger.info(f"[CoachService] Before commit: id={session.id}, user_id={user.id}, in_transaction={self.db.in_transaction()}")
        try:
            await self.db.commit()
            logger.info(f"[CoachService] Commit successful")
        except Exception as e:
            logger.error(f"[CoachService] Commit failed: {e}")
            raise

        logger.info(f"[CoachService] 创建会话: id={session.id}, user_id={user.id}")
        return session

    async def get_sessions(self, user: User) -> List[ChatSession]:
        """获取用户的会话列表"""
        result = await self.db.execute(
            select(ChatSession)
            .where(ChatSession.user_id == user.id)
            .where(ChatSession.status == ChatSessionStatus.ACTIVE)
            .order_by(ChatSession.updated_at.desc())
        )
        return list(result.scalars().all())

    async def get_session(self, session_id: int) -> Optional[ChatSession]:
        """获取会话详情"""
        result = await self.db.execute(
            select(ChatSession)
            .where(ChatSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def get_messages(self, session_id: int) -> List[ChatMessage]:
        """获取历史消息"""
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
        )
        return list(result.scalars().all())

    async def chat(self, user: User, session_id: int, message: str) -> dict:
        """发送消息（非流式）"""
        # 检查会话是否属于当前用户
        session = await self.get_session(session_id)
        if not session or session.user_id != user.id:
            raise BusinessException(*ErrorCode.SESSION_NOT_FOUND)

        # TODO: 积分扣除功能 - 需要先创建 t_point_log 表
        # # 检查积分
        # if user.points < 10:
        #     raise BusinessException(*ErrorCode.POINTS_NOT_ENOUGH)
        # # 扣除积分
        # await self.point_service.consume(user, 10, "AI教练对话")

        # 保存用户消息
        user_msg = ChatMessage(
            session_id=session_id,
            role="user",
            content=message,
            tokens=len(message) // 4,
        )
        self.db.add(user_msg)

        # 调用AI
        try:
            response = await self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": message}
                ]
            )

            ai_message = response.content[0].text

        except Exception as e:
            logger.error(f"[CoachService] AI调用失败: {str(e)}")
            ai_message = f"抱歉，AI服务暂时不可用。错误：{str(e)}"

        # 保存AI消息
        assistant_msg = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=ai_message,
            tokens=len(ai_message) // 4,
        )
        self.db.add(assistant_msg)

        # 更新会话
        session.message_count += 2
        session.total_tokens += user_msg.tokens + assistant_msg.tokens
        session.updated_at = datetime.utcnow()

        await self.db.commit()

        return {
            "role": "assistant",
            "content": ai_message,
            "tokens": assistant_msg.tokens
        }

    async def chat_stream_generator(
        self, user: User, session_id: int, message: str
    ):
        """发送消息（SSE流式生成器）- 简化版"""
        # 非流式实现
        result = await self.chat(user, session_id, message)
        yield f"data: {result}\n\n"
        yield "data: [DONE]\n\n"

    async def close_session(self, session_id: int):
        """关闭会话"""
        session = await self.get_session(session_id)
        if session:
            session.status = ChatSessionStatus.CLOSED
            session.updated_at = datetime.utcnow()
            await self.db.commit()
            logger.info(f"[CoachService] 关闭会话: id={session_id}")
