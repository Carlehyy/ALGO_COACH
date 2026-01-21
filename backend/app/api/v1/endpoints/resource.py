"""
Resource API端点
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Body, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.mysql import get_mysql_session
from app.api.deps import get_current_user, get_current_admin
from app.services.resource_service import ResourceService
from app.core.response import Response, PageResponse
from loguru import logger

router = APIRouter(prefix="/resources", tags=["资源管理"])


@router.post("/upload", response_model=Response)
async def upload_resource(
    type: str = Body(..., description="资源类型(pdf/video/blog/leetcode)"),
    title: str = Body(..., description="标题"),
    url: str = Body(None, description="URL链接"),
    file: UploadFile = File(None, description="文件"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """
    上传资源

    支持两种方式：
    1. 上传文件（PDF/视频）
    2. 提供URL（博客/LeetCode）
    """
    service = ResourceService(db)

    file_path = None
    file_size = None

    # 如果有文件，上传到MinIO
    if file and file.filename:
        try:
            # 读取文件内容
            content = await file.read()
            file_size = len(content)

            # 生成文件路径
            import uuid
            ext = file.filename.split('.')[-1] if '.' in file.filename else ''
            filename = f"{uuid.uuid4()}.{ext}"
            file_path = f"resources/{type}/{filename}"

            # 上传到MinIO
            from app.infrastructure.storage.minio_client import minio_client
            await minio_client.upload_file(
                file_path, content, file.content_type
            )

            logger.info(f"文件上传成功: {file_path}")
        except Exception as e:
            logger.error(f"文件上传失败: {e}")
            return Response.fail(code=60002, message="文件上传失败")

    # 创建资源记录
    resource = await service.create_resource(
        type=type,
        title=title,
        url=url or (file.filename if file else ""),
        uploader_id=current_user.id,
        file_path=file_path,
        file_size=file_size,
    )

    return Response.success(data=resource.to_dict(), message="资源上传成功")


@router.get("/", response_model=PageResponse)
async def get_resources(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type: Optional[str] = Query(None),
    process_status: Optional[str] = Query(None),
    review_status: Optional[str] = Query(None),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_session),
):
    """获取资源列表"""
    service = ResourceService(db)
    skip = (page - 1) * page_size
    resources, total = await service.get_resources(
        skip, page_size, type, process_status, review_status
    )
    resource_dicts = [r.to_dict() for r in resources]
    return PageResponse.create(items=resource_dicts, total=total, page=page, page_size=page_size)


@router.get("/{resource_id}", response_model=Response)
async def get_resource(
    resource_id: int,
    db: AsyncSession = Depends(get_mysql_session),
):
    """获取资源详情"""
    service = ResourceService(db)
    resource = await service.get_resource(resource_id)
    if not resource:
        return Response.fail(code=60001, message="资源不存在")
    return Response.success(data=resource.to_dict())


@router.put("/{resource_id}/status", response_model=Response)
async def update_status(
    resource_id: int,
    process_status: Optional[str] = Body(None),
    review_status: Optional[str] = Body(None),
    parse_result: Optional[str] = Body(None),
    current_admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_mysql_session),
):
    """更新资源状态"""
    service = ResourceService(db)
    resource = await service.update_status(
        resource_id, process_status, review_status, parse_result
    )
    if not resource:
        return Response.fail(code=60001, message="资源不存在")
    return Response.success(data=resource.to_dict(), message="状态更新成功")


@router.post("/{resource_id}/parse", response_model=Response)
async def trigger_parse(
    resource_id: int,
    current_admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_mysql_session),
):
    """触发解析任务"""
    # TODO: 创建Celery异步任务解析PDF
    service = ResourceService(db)
    resource = await service.update_status(resource_id, "processing")

    # 触发异步任务
    # from app.tasks.resource_tasks import parse_pdf_task
    # parse_pdf_task.delay(resource_id)

    return Response.success(data=resource.to_dict(), message="解析任务已触发")


@router.delete("/{resource_id}", response_model=Response)
async def delete_resource(
    resource_id: int,
    current_admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_mysql_session),
):
    """删除资源"""
    service = ResourceService(db)
    success = await service.delete_resource(resource_id)
    if not success:
        return Response.fail(code=60001, message="资源不存在")
    await db.commit()
    return Response.success(message="资源已删除")
