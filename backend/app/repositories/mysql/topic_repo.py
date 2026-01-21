"""
Topic数据访问层
"""

from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mysql.topic import Topic


class TopicRepository:
    """Topic数据访问类"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, topic_id: str) -> Optional[Topic]:
        """根据ID获取知识点"""
        result = await self.db.execute(select(Topic).where(Topic.id == topic_id))
        return result.scalar_one_or_none()

    async def get_all(self, status: str = "1") -> List[Topic]:
        """获取所有知识点"""
        result = await self.db.execute(
            select(Topic).where(Topic.status == status).order_by(Topic.category, Topic.importance.desc())
        )
        return list(result.scalars().all())

    async def get_by_category(self, category: str) -> List[Topic]:
        """根据分类获取知识点"""
        result = await self.db.execute(
            select(Topic)
            .where(Topic.category == category, Topic.status == "1")
            .order_by(Topic.difficulty)
        )
        return list(result.scalars().all())

    async def get_prerequisites(self, topic_id: str) -> List[Topic]:
        """获取前置知识点"""
        topic = await self.get_by_id(topic_id)
        if not topic or not topic.prerequisites:
            return []

        result = await self.db.execute(
            select(Topic).where(Topic.id.in_(topic.prerequisites))
        )
        return list(result.scalars().all())

    async def get_related(self, topic_id: str) -> List[Topic]:
        """获取相关知识点"""
        topic = await self.get_by_id(topic_id)
        if not topic or not topic.related:
            return []

        result = await self.db.execute(
            select(Topic).where(Topic.id.in_(topic.related))
        )
        return list(result.scalars().all())

    async def create(self, topic: Topic) -> Topic:
        """创建知识点"""
        self.db.add(topic)
        await self.db.flush()
        await self.db.refresh(topic)
        return topic

    async def batch_create(self, topics: List[Topic]) -> None:
        """批量创建知识点"""
        self.db.add_all(topics)
        await self.db.flush()

    async def update(self, topic: Topic) -> Topic:
        """更新知识点"""
        await self.db.flush()
        await self.db.refresh(topic)
        return topic
