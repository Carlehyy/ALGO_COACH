"""
Topic业务逻辑层
"""

from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models.mysql.topic import Topic
from app.repositories.mysql.topic_repo import TopicRepository
from loguru import logger


class TopicService:
    """Topic业务逻辑类"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.topic_repo = TopicRepository(db)

    async def get_topic_detail(self, topic_id: str) -> Optional[Dict]:
        """获取知识点详情（包含前置和相关）"""
        topic = await self.topic_repo.get_by_id(topic_id)
        if not topic:
            return None

        # 获取前置知识点
        prerequisites = await self.topic_repo.get_prerequisites(topic_id)

        # 获取相关知识点
        related = await self.topic_repo.get_related(topic_id)

        return {
            **topic.to_dict(),
            "prerequisites_detail": [p.to_dict() for p in prerequisites],
            "related_detail": [r.to_dict() for r in related],
        }

    async def get_topic_tree(self) -> Dict:
        """获取知识点树状结构"""
        from app.config import settings

        categories = {
            "basic": "基础算法",
            "data_structure": "数据结构",
            "dp": "动态规划",
            "graph": "图论",
            "string": "字符串",
            "math": "数学",
        }

        tree = {}
        for cat_id, cat_name in categories.items():
            topics = await self.topic_repo.get_by_category(cat_id)
            tree[cat_id] = {
                "name": cat_name,
                "topics": [t.to_dict() for t in topics],
            }

        return tree

    async def check_prerequisites(self, topic_id: str, learned_topics: List[str]) -> Dict:
        """检查是否满足前置条件"""
        topic = await self.topic_repo.get_by_id(topic_id)
        if not topic:
            return {"satisfied": False, "missing": []}

        prerequisites = topic.prerequisites or []
        missing = [p for p in prerequisites if p not in learned_topics]

        return {
            "satisfied": len(missing) == 0,
            "missing": missing,
        }

    async def get_learning_path(self, target_topic: str) -> List[str]:
        """生成到目标知识点的学习路径"""
        # TODO: 实现拓扑排序生成学习路径
        topic = await self.topic_repo.get_by_id(target_topic)
        if not topic:
            return []

        # 简化版：直接返回前置知识点链
        path = []
        visited = set()

        def collect_prereqs(topic_id):
            if topic_id in visited:
                return
            visited.add(topic_id)
            topic = await self.topic_repo.get_by_id(topic_id)
            if topic and topic.prerequisites:
                for prereq in topic.prerequisites:
                    collect_prereqs(prereq)
            path.append(topic_id)

        collect_prereqs(target_topic)
        return path
