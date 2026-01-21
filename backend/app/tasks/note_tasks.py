"""
笔记生成Celery任务
参考：开发指南V3 - 6.8 异步任务
"""

from celery import shared_task
from loguru import logger

from app.infrastructure.database.mysql import get_mysql_session
from app.services.note_generation_service import NoteGenerationService
from app.models.mysql.resource import Resource


@shared_task(bind=True, max_retries=3)
def generate_note_task(self, topic_id: str, resource_ids: list = None):
    """
    异步生成笔记任务

    Args:
        topic_id: 知识点ID
        resource_ids: 关联资源ID列表
    """
    logger.info(f"[Celery] 开始执行笔记生成任务: topic_id={topic_id}")

    try:
        # 获取数据库会话
        db = get_mysql_session()

        # 创建服务实例
        service = NoteGenerationService(db)

        # 生成笔记
        import asyncio
        note = asyncio.run(service.generate_note_for_topic(
            topic_id=topic_id,
            resource_ids=resource_ids,
            regenerate=True
        ))

        logger.info(f"[Celery] 笔记生成任务完成: topic_id={topic_id}, note_id={note.id}")

        return {
            "status": "success",
            "topic_id": topic_id,
            "note_id": str(note.id),
            "quality_score": note.quality_score
        }

    except Exception as e:
        logger.error(f"[Celery] 笔记生成任务失败: topic_id={topic_id}, error={str(e)}")

        # 重试
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))

        return {
            "status": "failed",
            "topic_id": topic_id,
            "error": str(e)
        }


@shared_task(bind=True)
def parse_resource_task(self, resource_id: int):
    """
    解析资源任务（PDF/视频等）

    Args:
        resource_id: 资源ID
    """
    logger.info(f"[Celery] 开始执行资源解析任务: resource_id={resource_id}")

    try:
        db = get_mysql_session()

        # 获取资源
        from sqlalchemy import select
        result = db.execute(select(Resource).where(Resource.id == resource_id))
        resource = result.scalar_one_or_none()

        if not resource:
            raise ValueError(f"资源不存在: {resource_id}")

        # TODO: 实际解析逻辑
        # - PDF: 提取文本、图片、代码
        # - 视频: 提取字幕、关键帧
        # - 博客: 抓取内容

        # 模拟解析结果
        parse_result = f"""
# {resource.title}

## 解析内容

这里是从资源中提取的内容...

## 代码示例

```python
def example():
    pass
```
"""

        # 更新资源状态
        from app.services.resource_service import ResourceService
        resource_service = ResourceService(db)

        import asyncio
        asyncio.run(resource_service.update_status(
            resource_id=resource_id,
            process_status="completed",
            parse_result=parse_result
        ))

        logger.info(f"[Celery] 资源解析任务完成: resource_id={resource_id}")

        return {
            "status": "success",
            "resource_id": resource_id
        }

    except Exception as e:
        logger.error(f"[Celery] 资源解析任务失败: resource_id={resource_id}, error={str(e)}")

        # 更新状态为失败
        try:
            db = get_mysql_session()
            from app.services.resource_service import ResourceService
            resource_service = ResourceService(db)

            import asyncio
            asyncio.run(resource_service.update_status(
                resource_id=resource_id,
                process_status="failed"
            ))
        except:
            pass

        return {
            "status": "failed",
            "resource_id": resource_id,
            "error": str(e)
        }


@shared_task
def batch_generate_notes(topic_ids: list):
    """
    批量生成笔记任务

    Args:
        topic_ids: 知识点ID列表
    """
    logger.info(f"[Celery] 开始批量生成笔记: count={len(topic_ids)}")

    results = []
    for topic_id in topic_ids:
        try:
            result = generate_note_task(topic_id)
            results.append(result)
        except Exception as e:
            logger.error(f"[Celery] 批量生成失败: topic_id={topic_id}, error={str(e)}")
            results.append({
                "status": "failed",
                "topic_id": topic_id,
                "error": str(e)
            })

    success_count = sum(1 for r in results if r.get("status") == "success")
    logger.info(f"[Celery] 批量生成完成: success={success_count}/{len(topic_ids)}")

    return {
        "status": "completed",
        "total": len(topic_ids),
        "success": success_count,
        "failed": len(topic_ids) - success_count,
        "results": results
    }
