"""
Note数据访问层 (MongoDB)
"""

from typing import Optional, List
from beanie import PydanticObjectId

from app.models.mongo.note import Note


class NoteRepository:
    """Note数据访问类"""

    async def get_by_id(self, note_id: str) -> Optional[Note]:
        """根据ID获取笔记"""
        return await Note.get(note_id)

    async def get_by_topic_id(self, topic_id: str, status: int = 2) -> List[Note]:
        """根据知识点ID获取笔记"""
        return await Note.find(
            Note.topic_id == topic_id,
            Note.status == status
        ).to_list()

    async def search(self, keyword: str, limit: int = 20) -> List[Note]:
        """全文搜索笔记"""
        # 简化版搜索：搜索标题和摘要
        return await Note.find(
            {
                "$or": [
                    {"title": {"$regex": keyword, "$options": "i"}},
                    {"summary": {"$regex": keyword, "$options": "i"}},
                ],
                "status": 2,
            }
        ).limit(limit).to_list()

    async def get_published_notes(
        self, skip: int = 0, limit: int = 20
    ) -> tuple[List[Note], int]:
        """获取已发布的笔记（分页）"""
        notes = await Note.find(
            Note.status == 2
        ).sort(-Note.created_at).skip(skip).limit(limit).to_list()

        total = await Note.find(Note.status == 2).count()

        return notes, total

    async def create(self, note: Note) -> Note:
        """创建笔记"""
        await note.save()
        return note

    async def update(self, note: Note) -> Note:
        """更新笔记"""
        await note.save()
        return note

    async def increment_view_count(self, note_id: str) -> None:
        """增加浏览次数"""
        note = await self.get_by_id(note_id)
        if note:
            note.view_count += 1
            await note.save()
