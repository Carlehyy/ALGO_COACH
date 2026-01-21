"""
NoteGenerationService - 笔记生成服务
参考：开发指南V3 - 6.8 异步任务
"""

import json
from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.mysql.topic import Topic
from app.models.mysql.resource import Resource, ResourceType
from app.models.mongo.note import Note
from app.infrastructure.ai.claude_client import MockClaudeClient
from app.prompts.note_prompts import NotePrompts
from loguru import logger


class NoteGenerationService:
    """笔记生成服务类"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.claude_client = MockClaudeClient()

    async def generate_note_for_topic(
        self,
        topic_id: str,
        resource_ids: Optional[list] = None,
        regenerate: bool = False
    ) -> Note:
        """
        为指定知识点生成完整笔记（L1-L4）

        Args:
            topic_id: 知识点ID
            resource_ids: 使用的资源ID列表
            regenerate: 是否重新生成

        Returns:
            生成的Note对象
        """
        # 获取知识点信息
        topic = await self._get_topic(topic_id)
        if not topic:
            raise ValueError(f"知识点不存在: {topic_id}")

        # 检查是否已有笔记
        existing_note = await self._get_existing_note(topic_id)
        if existing_note and not regenerate:
            logger.info(f"[NoteGeneration] 笔记已存在: {topic_id}")
            return existing_note

        # 准备资源摘要
        resource_summary = await self._prepare_resource_summary(
            resource_ids or [],
            topic_id
        )

        # 生成各层级内容
        logger.info(f"[NoteGeneration] 开始生成笔记: {topic_id}")

        l1_content = await self._generate_l1(topic, resource_summary)
        logger.info(f"[NoteGeneration] L1生成完成: {topic_id}")

        l2_content = await self._generate_l2(topic)
        logger.info(f"[NoteGeneration] L2生成完成: {topic_id}")

        l3_content = await self._generate_l3(topic, resource_summary)
        logger.info(f"[NoteGeneration] L3生成完成: {topic_id}")

        l4_content = await self._generate_l4(topic)
        logger.info(f"[NoteGeneration] L4生成完成: {topic_id}")

        # 质量评估
        quality_score = await self._evaluate_quality(
            topic_id, l1_content, l2_content, l3_content, l4_content
        )
        logger.info(f"[NoteGeneration] 质量评估完成: {topic_id}, 分数: {quality_score}")

        # 创建或更新笔记
        if existing_note and regenerate:
            note = existing_note
            note.content_l1 = l1_content
            note.content_l2 = l2_content
            note.content_l3 = l3_content
            note.content_l4 = l4_content
            note.quality_score = quality_score
            note.status = 1  # 待审核
            await note.save()
        else:
            note = await Note(
                topic_id=topic_id,
                content_l1=l1_content,
                content_l2=l2_content,
                content_l3=l3_content,
                content_l4=l4_content,
                quality_score=quality_score,
                status=1,  # 待审核
                resource_ids=resource_ids or []
            ).create()

        logger.info(f"[NoteGeneration] 笔记生成完成: {topic_id}")
        return note

    async def _get_topic(self, topic_id: str) -> Optional[Topic]:
        """获取知识点信息"""
        result = await self.db.execute(
            select(Topic).where(Topic.id == topic_id)
        )
        return result.scalar_one_or_none()

    async def _get_existing_note(self, topic_id: str) -> Optional[Note]:
        """获取已存在的笔记"""
        try:
            return await Note.find_one({"topic_id": topic_id})
        except:
            return None

    async def _prepare_resource_summary(self, resource_ids: list, topic_id: str) -> Dict:
        """准备资源摘要"""
        if not resource_ids:
            return {
                "summary": f"关于{topic_id}的学习资料",
                "code_snippets": "",
                "examples": []
            }

        resources = []
        code_snippets_list = []

        for rid in resource_ids:
            result = await self.db.execute(
                select(Resource).where(Resource.id == rid)
            )
            resource = result.scalar_one_or_none()
            if resource:
                resources.append({
                    "type": resource.type,
                    "title": resource.title,
                    "parse_result": resource.parse_result
                })
                # 提取代码片段（如果存在）
                if resource.parse_result:
                    # TODO: 实际应该解析parse_result提取代码
                    code_snippets_list.append(f"# 来自 {resource.title}")

        return {
            "summary": json.dumps(resources, ensure_ascii=False),
            "code_snippets": "\n\n".join(code_snippets_list),
            "examples": []
        }

    async def _generate_l1(self, topic: Topic, resource_summary: Dict) -> str:
        """生成L1层内容 - 直观引入"""
        prompt = NotePrompts.format_l1_prompt(
            topic_id=topic.id,
            description=topic.description or "",
            difficulty=topic.difficulty,
            related_topics=topic.related or [],
            resource_summary=resource_summary["summary"]
        )

        response = await self.claude_client.chat(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response["content"]

    async def _generate_l2(self, topic: Topic) -> str:
        """生成L2层内容 - 核心原理"""
        prompt = NotePrompts.format_l2_prompt(
            topic_id=topic.id,
            description=topic.description or "",
            difficulty=topic.difficulty,
            prerequisites=topic.prerequisites or [],
            related_topics=topic.related or []
        )

        response = await self.claude_client.chat(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response["content"]

    async def _generate_l3(self, topic: Topic, resource_summary: Dict) -> str:
        """生成L3层内容 - 代码实现"""
        prompt = NotePrompts.format_l3_prompt(
            topic_id=topic.id,
            description=topic.description or "",
            code_snippets=resource_summary["code_snippets"]
        )

        response = await self.claude_client.chat(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response["content"]

    async def _generate_l4(self, topic: Topic) -> str:
        """生成L4层内容 - 实战分析"""
        # TODO: 从数据库获取相关题目
        related_problems = [
            f"{topic.id} - 经典应用题1",
            f"{topic.id} - 经典应用题2"
        ]

        prompt = NotePrompts.format_l4_prompt(
            topic_id=topic.id,
            description=topic.description or "",
            related_problems=related_problems
        )

        response = await self.claude_client.chat(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response["content"]

    async def _evaluate_quality(
        self,
        topic_id: str,
        l1_content: str,
        l2_content: str,
        l3_content: str,
        l4_content: str
    ) -> int:
        """评估笔记质量"""
        prompt = NotePrompts.format_quality_prompt(
            topic_id=topic_id,
            l1_content=l1_content,
            l2_content=l2_content,
            l3_content=l3_content,
            l4_content=l4_content
        )

        response = await self.claude_client.chat(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        # 解析质量评分
        try:
            content = response["content"]
            # 提取JSON部分
            if "```json" in content:
                json_start = content.index("```json") + 7
                json_end = content.index("```", json_start)
                json_str = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.index("```") + 3
                json_end = content.index("```", json_start)
                json_str = content[json_start:json_end].strip()
            else:
                json_str = content.strip()

            result = json.loads(json_str)
            return result.get("total_score", 75)
        except Exception as e:
            logger.warning(f"[NoteGeneration] 质量评估解析失败: {e}")
            return 75  # 默认分数

    async def generate_single_layer(
        self,
        topic_id: str,
        layer: str,
        resource_ids: Optional[list] = None
    ) -> str:
        """
        生成单个层级的内容

        Args:
            topic_id: 知识点ID
            layer: 层级 (l1/l2/l3/l4)
            resource_ids: 资源ID列表

        Returns:
            生成的内容
        """
        topic = await self._get_topic(topic_id)
        if not topic:
            raise ValueError(f"知识点不存在: {topic_id}")

        resource_summary = await self._prepare_resource_summary(
            resource_ids or [],
            topic_id
        )

        if layer == "l1":
            return await self._generate_l1(topic, resource_summary)
        elif layer == "l2":
            return await self._generate_l2(topic)
        elif layer == "l3":
            return await self._generate_l3(topic, resource_summary)
        elif layer == "l4":
            return await self._generate_l4(topic)
        else:
            raise ValueError(f"无效的层级: {layer}")
