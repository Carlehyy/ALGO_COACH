"""
ResourceService - 资源管理业务逻辑
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.models.mysql.resource import Resource, ResourceType, ProcessStatus, ReviewStatus
from app.infrastructure.storage.minio_client import minio_client
from loguru import logger


class ResourceService:
    """资源业务逻辑类"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_resource(self, resource_id: int) -> Optional[Resource]:
        """根据ID获取资源"""
        result = await self.db.execute(
            select(Resource).where(Resource.id == resource_id)
        )
        return result.scalar_one_or_none()

    async def get_resources(
        self,
        skip: int = 0,
        limit: int = 20,
        type: Optional[str] = None,
        process_status: Optional[str] = None,
        review_status: Optional[str] = None,
    ) -> tuple[List[Resource], int]:
        """获取资源列表"""
        query = select(Resource)

        # 筛选条件
        if type:
            query = query.where(Resource.type == type)
        if process_status:
            query = query.where(Resource.process_status == process_status)
        if review_status:
            query = query.where(Resource.review_status == review_status)

        # 获取总数
        count_query = select(Resource.id)
        if type:
            count_query = count_query.where(Resource.type == type)
        if process_status:
            count_query = count_query.where(Resource.process_status == process_status)
        if review_status:
            count_query = count_query.where(Resource.review_status == review_status)

        count_result = await self.db.execute(count_query)
        total = len(count_result.all())

        # 分页
        query = query.order_by(Resource.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        resources = result.scalars().all()

        return list(resources), total

    async def create_resource(
        self,
        type: str,
        title: str,
        url: str,
        uploader_id: int,
        file_path: Optional[str] = None,
        file_size: Optional[int] = None,
    ) -> Resource:
        """创建资源记录"""
        resource = Resource(
            type=type,
            title=title,
            url=url,
            file_path=file_path,
            file_size=file_size,
            process_status=ProcessStatus.PENDING,
            uploader_id=uploader_id,
        )
        self.db.add(resource)
        await self.db.flush()
        await self.db.refresh(resource)

        logger.info(f"[ResourceService] 创建资源: id={resource.id}, type={type}, title={title}")
        return resource

    async def update_status(
        self,
        resource_id: int,
        process_status: Optional[str] = None,
        review_status: Optional[str] = None,
        parse_result: Optional[str] = None,
    ) -> Resource:
        """更新资源状态"""
        resource = await self.get_resource(resource_id)
        if not resource:
            return None

        if process_status:
            resource.process_status = process_status
        if review_status:
            resource.review_status = review_status
        if parse_result is not None:
            resource.parse_result = parse_result

        if process_status == "completed":
            resource.processed_at = datetime.utcnow()

        await self.db.flush()
        await self.db.refresh(resource)

        logger.info(f"[ResourceService] 更新资源状态: id={resource_id}, status={process_status}")
        return resource

    async def delete_resource(self, resource_id: int) -> bool:
        """删除资源"""
        resource = await self.get_resource(resource_id)
        if not resource:
            return False

        # 如果有文件，也从MinIO删除
        if resource.file_path:
            try:
                await minio_client.delete_file(resource.file_path)
            except Exception as e:
                logger.warning(f"[ResourceService] 删除MinIO文件失败: {e}")

        await self.db.delete(resource)
        logger.info(f"[ResourceService] 删除资源: id={resource_id}")
        return True

    async def get_pending_resources(self) -> List[Resource]:
        """获取待处理的资源"""
        result = await self.db.execute(
            select(Resource)
            .where(Resource.process_status == ProcessStatus.PENDING)
            .order_by(Resource.created_at.asc())
        )
        return list(result.scalars().all())
