"""
ACM算法学习平台 - MinIO对象存储客户端
参考：开发指南V3 - 6.7 数据库连接
"""

from io import BytesIO
from typing import Optional
from minio import Minio
from minio.error import S3Error
from loguru import logger

from app.config import settings


class MinIOClient:
    """MinIO客户端封装"""

    def __init__(self):
        self.client: Minio = None
        self.bucket = settings.minio_bucket

    async def init(self):
        """初始化MinIO客户端"""
        logger.info(f"正在连接MinIO: {settings.minio_endpoint}:{settings.minio_port}")

        endpoint = f"{settings.minio_endpoint}:{settings.minio_port}"
        access_key = settings.minio_access_key
        secret_key = settings.minio_secret_key
        secure = settings.minio_secure

        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)

        # 创建存储桶（如果不存在）
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)
            logger.info(f"MinIO存储桶创建成功: {self.bucket}")
        else:
            logger.info(f"MinIO存储桶已存在: {self.bucket}")

        logger.info("MinIO客户端初始化成功")

    async def upload_file(
        self, object_name: str, data: bytes, content_type: Optional[str] = None
    ) -> bool:
        """上传文件"""
        try:
            data_stream = BytesIO(data)
            length = len(data)

            self.client.put_object(
                self.bucket,
                object_name,
                data_stream,
                length,
                content_type=content_type,
            )

            logger.info(f"MinIO文件上传成功: {object_name}")
            return True
        except S3Error as e:
            logger.error(f"MinIO文件上传失败: {e}")
            return False

    async def download_file(self, object_name: str) -> Optional[bytes]:
        """下载文件"""
        try:
            response = self.client.get_object(self.bucket, object_name)
            data = response.read()
            logger.info(f"MinIO文件下载成功: {object_name}")
            return data
        except S3Error as e:
            logger.error(f"MinIO文件下载失败: {e}")
            return None

    async def get_presigned_url(self, object_name: str, expires: int = 3600) -> Optional[str]:
        """获取预签名URL"""
        try:
            url = self.client.presigned_get_object(self.bucket, object_name, expires=expires)
            return url
        except S3Error as e:
            logger.error(f"MinIO获取预签名URL失败: {e}")
            return None

    async def delete_file(self, object_name: str) -> bool:
        """删除文件"""
        try:
            self.client.remove_object(self.bucket, object_name)
            logger.info(f"MinIO文件删除成功: {object_name}")
            return True
        except S3Error as e:
            logger.error(f"MinIO文件删除失败: {e}")
            return False

    async def file_exists(self, object_name: str) -> bool:
        """检查文件是否存在"""
        try:
            self.client.stat_object(self.bucket, object_name)
            return True
        except S3Error:
            return False


# 全局MinIO客户端实例
minio_client = MinIOClient()


async def init_minio():
    """初始化MinIO客户端"""
    await minio_client.init()


async def close_minio():
    """关闭MinIO客户端（MinIO客户端不需要显式关闭）"""
    pass
