"""
ACM算法学习平台 - 配置管理
使用 Pydantic Settings 管理应用配置
参考：开发指南V3 - 6.2 项目配置
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # === 应用配置 ===
    app_name: str = "acm-learning-platform"
    app_env: str = "development"
    app_debug: bool = True
    app_secret_key: str = "change-this-secret-key"

    # === MySQL配置 ===
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "acm_user"
    mysql_password: str = "acm_password"
    mysql_database: str = "acm_platform"

    @property
    def mysql_url(self) -> str:
        """MySQL连接URL"""
        return f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"

    # === SQLite配置 ===
    sqlite_url: str = "sqlite+aiosqlite:///./acm_platform.db"

    # === MongoDB配置 ===
    mongodb_host: str = "localhost"
    mongodb_port: int = 27017
    mongodb_user: str = "acm_user"
    mongodb_password: str = "acm_password"
    mongodb_database: str = "acm_platform"

    @property
    def mongodb_url(self) -> str:
        """MongoDB连接URL"""
        return f"mongodb://{self.mongodb_user}:{self.mongodb_password}@{self.mongodb_host}:{self.mongodb_port}/{self.mongodb_database}"

    # === Redis配置 ===
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0

    @property
    def redis_url(self) -> str:
        """Redis连接URL"""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # === MinIO配置 ===
    minio_endpoint: str = "localhost"
    minio_port: int = 9000
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_secure: bool = False
    minio_bucket: str = "acm-platform"

    # === JWT配置 ===
    jwt_secret_key: str = "change-this-jwt-secret"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_days: int = 7

    # === Claude AI配置 ===
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    anthropic_max_tokens: int = 4096

    # === DeepSeek AI配置（备选）===
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"

    # === Celery配置 ===
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # === 日志配置 ===
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    error_log_file: str = "logs/error.log"

    # === CORS配置 ===
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # === 积分配置 ===
    coach_points_per_message: int = 10
    points_per_million_tokens: int = 100
    new_user_bonus_points: int = 100

    # === 文件上传配置 ===
    max_upload_size: int = 104857600  # 100MB
    allowed_file_types: str = "pdf,mp4,mp3"


@lru_cache
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


# 全局配置实例
settings = get_settings()
