"""
Note业务逻辑层
"""

from typing import List, Optional
from datetime import datetime

from app.models.mongo.note import Note
from app.repositories.mongo.note_repo import NoteRepository
from loguru import logger


class NoteService:
    """Note业务逻辑类"""

    def __init__(self):
        self.note_repo = NoteRepository()

    async def get_note(self, note_id: str) -> Optional[Note]:
        """获取笔记详情"""
        note = await self.note_repo.get_by_id(note_id)
        if note:
            # 增加浏览次数
            await self.note_repo.increment_view_count(note_id)
        return note

    async def get_notes_by_topic(self, topic_id: str) -> List[Note]:
        """根据知识点获取笔记"""
        return await self.note_repo.get_by_topic_id(topic_id)

    async def search_notes(self, keyword: str, limit: int = 20) -> List[Note]:
        """搜索笔记"""
        return await self.note_repo.search(keyword, limit)

    async def get_published_notes(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[List[Note], int]:
        """获取已发布的笔记"""
        skip = (page - 1) * page_size
        return await self.note_repo.get_published_notes(skip, page_size)

    async def create_note(self, note_data: dict) -> Note:
        """创建笔记"""
        note = Note(**note_data)
        note = await self.note_repo.create(note)
        logger.info(f"[NoteService] 创建笔记: id={note.id}")
        return note

    async def publish_note(self, note_id: str) -> Note:
        """发布笔记"""
        note = await self.note_repo.get_by_id(note_id)
        if note:
            note.status = 2
            note.published_at = datetime.utcnow()
            note = await self.note_repo.update(note)
            logger.info(f"[NoteService] 发布笔记: id={note_id}")
        return note
