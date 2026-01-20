# CLAUDE.md - ACM算法学习平台项目配置

> **项目代号**: acm-learning-platform  
> **版本**: V1.0  
> **最后更新**: 2026年1月  
> **适用于**: Claude Code / AI Agent 开发

---

## 🎯 项目概述

你正在开发 **ACM算法学习平台** —— 一个AI驱动的个性化算法学习平台。

### 核心价值

```
📚 多源资料 → 🤖 AI融合 → 📝 分层笔记 → 🎯 个性化学习
```

### 产品定位

将多源学习资料（书籍PDF、博客、视频、LeetCode题解）通过AI融合，生成由浅入深的高质量学习笔记：

- **L1 直观引入**: 生活类比、动画演示、快速建立直觉
- **L2 核心原理**: 严谨推导、数学证明、深入理解本质
- **L3 代码实现**: 逐行注释、复杂度分析、工程实践
- **L4 实战分析**: 例题精讲、变体总结、举一反三

### 核心功能模块

| 模块 | 优先级 | 说明 |
|------|--------|------|
| 智能笔记系统 | P0 | 多源数据融合，L1-L4分层笔记生成 |
| 知识图谱 | P0 | 算法知识点结构化管理 |
| 管理后台 | P0 | 资源上传、PDF校对、内容审核 |
| AI教练系统 | P1 | 智能问答、学习计划生成 |
| 积分系统 | P1 | 充值、消费、权限控制 |
| 科学能力评估 | P1 | 六维度评估 + AI测评 |

---

## 🛠️ 技术栈

### 后端 (Python)

```yaml
语言: Python 3.11+
框架: FastAPI 0.109+
ASGI: Uvicorn
数据验证: Pydantic 2.0
MySQL ORM: SQLAlchemy 2.0 (异步)
MongoDB ODM: Beanie 1.25+ (基于Motor)
缓存: Redis 7 (redis-py)
任务队列: Celery 5.3
认证: python-jose (JWT) + passlib (bcrypt)
日志: Loguru
AI SDK: anthropic (Claude API)
对象存储: minio
```

### 前端

```yaml
框架: uipro (UI/UX Pro Max)
初始化: uipro init --ai claude
官网: https://ui.cod.ndjp.net/
构建: Vite 5 + Vue 3 + TypeScript
状态管理: Pinia
```

### 数据存储

```yaml
结构化数据: MySQL 8.0
  - 用户、订单、积分、知识点元数据
  
非结构化数据: MongoDB 6.0
  - 笔记内容、AI对话、日志文档
  
缓存: Redis 7.0
  - 会话缓存、热点数据、消息队列
  
对象存储: MinIO
  - PDF文件、图片、视频
  
向量数据库: ChromaDB
  - 笔记向量、语义检索
```

---

## 📁 项目目录结构

```
acm-learning-platform/
├── docs/                           # 📚 项目文档
│   ├── PRD-V4.md                   # 需求文档
│   ├── API.md                      # API文档
│   └── DATABASE.md                 # 数据库文档
│
├── backend/                        # 🐍 Python后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI入口
│   │   ├── config.py               # Pydantic Settings配置
│   │   │
│   │   ├── api/v1/                 # API路由层
│   │   │   ├── router.py           # 路由汇总
│   │   │   ├── deps.py             # 依赖注入
│   │   │   ├── endpoints/          # 各模块端点
│   │   │   │   ├── user.py
│   │   │   │   ├── note.py
│   │   │   │   ├── topic.py
│   │   │   │   ├── point.py
│   │   │   │   ├── coach.py
│   │   │   │   ├── resource.py
│   │   │   │   └── admin.py
│   │   │   └── schemas/            # Pydantic模式
│   │   │
│   │   ├── core/                   # 核心模块
│   │   │   ├── security.py         # JWT认证
│   │   │   ├── exceptions.py       # 异常处理
│   │   │   ├── response.py         # 统一响应
│   │   │   └── logging.py          # 日志配置
│   │   │
│   │   ├── models/                 # 数据模型
│   │   │   ├── mysql/              # SQLAlchemy模型
│   │   │   └── mongo/              # Beanie文档
│   │   │
│   │   ├── services/               # 业务逻辑层
│   │   ├── repositories/           # 数据访问层
│   │   │
│   │   ├── infrastructure/         # 基础设施
│   │   │   ├── database/           # 数据库连接
│   │   │   ├── cache/              # Redis
│   │   │   ├── storage/            # MinIO
│   │   │   ├── ai/                 # AI客户端
│   │   │   └── vector/             # 向量数据库
│   │   │
│   │   ├── tasks/                  # Celery异步任务
│   │   └── prompts/                # AI Prompt模板
│   │
│   ├── tests/                      # 单元测试
│   ├── scripts/                    # 脚本工具
│   ├── alembic/                    # 数据库迁移
│   ├── logs/                       # 日志目录
│   ├── requirements.txt
│   └── .env
│
├── frontend/                       # 🎨 前端应用
│   ├── src/
│   │   ├── api/                    # API请求
│   │   ├── components/             # 组件
│   │   ├── pages/                  # 页面
│   │   ├── stores/                 # 状态管理
│   │   ├── router/                 # 路由
│   │   └── utils/                  # 工具函数
│   └── package.json
│
├── landing-page/                   # 宣传页面
├── docker/                         # Docker配置
├── scripts/                        # 项目脚本
└── knowledge-skeleton/             # 知识图谱骨架
```

---

## 📋 开发规范

### 1. Git工作流

```bash
# 分支策略：双分支
master  # 稳定版本，只能通过合并dev
dev     # 开发分支，所有功能在此开发

# 开发流程
git checkout dev
git pull origin dev
# ... 开发 ...
# ... 测试通过 ...
git add .
git commit -m "<type>(<scope>): <subject>"
git push origin dev

# 发布时
git checkout master
git merge dev
git tag -a v1.x.x -m "Release v1.x.x"
git push origin master --tags
```

### 2. 提交信息规范

```
<type>(<scope>): <subject>

类型(type):
- feat: 新功能
- fix: Bug修复
- docs: 文档更新
- style: 代码格式
- refactor: 重构
- test: 测试
- chore: 构建/工具

示例:
feat(user): 实现用户注册和登录功能
fix(note): 修复Markdown渲染错误
test(point): 添加积分服务单元测试
```

### 3. 代码规范

#### Python后端

```python
# 统一响应格式
from app.core.response import Response

@router.get("/users/{id}")
async def get_user(id: int):
    user = await user_service.get_by_id(id)
    return Response.success(data=user)

# 异常处理
from app.core.exceptions import BusinessException, ErrorCode

if not user:
    raise BusinessException(*ErrorCode.USER_NOT_FOUND)

# 日志记录
from loguru import logger

logger.info(f"[USER][LOGIN] userId={user.id}, ip={ip}")
logger.error(f"[AI][ERROR] 调用失败, error={str(e)}")
```

#### 前端 (uipro)

```vue
<!-- 使用uipro组件 -->
<template>
  <UContainer>
    <UCard>
      <template #header>标题</template>
      内容
    </UCard>
    <UButton @click="handleClick">按钮</UButton>
  </UContainer>
</template>
```

### 4. 测试规范

```bash
# 运行测试（必须在提交前执行）
cd backend
pytest tests/ -v --cov=app --cov-report=term

# 覆盖率要求
Service层: > 80%
核心业务: > 90%

# 测试通过后才能提交
```

---

## ⚡ 开发命令速查

### 后端

```bash
# 进入后端目录
cd backend

# 激活虚拟环境
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --port 8000

# 运行测试
pytest tests/ -v --cov=app

# 数据库迁移
alembic revision --autogenerate -m "description"
alembic upgrade head

# 启动Celery Worker
celery -A app.tasks.celery_app worker --loglevel=info
```

### 前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器（自动打开浏览器）
npm run dev

# 使用uipro生成组件
uipro generate component "组件描述"
uipro generate page "页面描述"
uipro generate form "表单描述"

# 构建生产版本
npm run build
```

### Docker

```bash
# 启动开发环境服务
docker-compose -f docker/docker-compose.dev.yml up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 📊 当前开发阶段

### Phase 1: 基础架构 (Week 1-2) ⬜ 进行中

**目标**: 搭建后端骨架、前端骨架、完成用户系统

#### 后端骨架任务

```
⬜ 1.1.1  创建Python虚拟环境
⬜ 1.1.2  创建requirements.txt
⬜ 1.1.6  创建Pydantic Settings配置 (app/config.py)
⬜ 1.1.7  创建FastAPI应用入口 (app/main.py)
⬜ 1.1.8  实现统一响应格式 (app/core/response.py)
⬜ 1.1.9  实现全局异常处理 (app/core/exceptions.py)
⬜ 1.1.10 配置日志系统 (app/core/logging.py)
⬜ 1.1.11 实现JWT认证模块 (app/core/security.py)
⬜ 1.1.12 配置MySQL异步连接 (app/infrastructure/database/mysql.py)
⬜ 1.1.13 配置MongoDB异步连接 (app/infrastructure/database/mongo.py)
⬜ 1.1.14 配置Redis客户端 (app/infrastructure/cache/redis.py)
⬜ 1.1.15 配置MinIO客户端 (app/infrastructure/storage/minio_client.py)
```

#### 用户系统任务

```
⬜ 1.3.1  创建User模型 (app/models/mysql/user.py)
⬜ 1.3.5  创建UserService (app/services/user_service.py)
⬜ 1.3.6  编写UserService单元测试 ⚠️必须 (tests/test_services/test_user_service.py)
⬜ 1.3.7  创建用户API端点 (app/api/v1/endpoints/user.py)
```

### 下一阶段预览

```
Phase 2: 核心功能 (Week 3-6)
  - 知识点模块
  - 笔记模块 (L1-L4)
  - 积分系统
  - AI教练

Phase 3: 管理后台 (Week 7-8)
  - 资源管理
  - PDF校对器
  - 笔记生成引擎
  
Phase 4: 收尾发布 (Week 9-10)
  - 宣传页面
  - 文档完善
  - 测试部署
```

---

## 🔧 核心代码模板

### 1. 配置管理 (config.py)

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    
    # 应用配置
    app_name: str = "acm-learning-platform"
    app_env: str = "development"
    app_debug: bool = True
    app_secret_key: str
    
    # MySQL
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str
    mysql_database: str = "acm_platform"
    
    @property
    def mysql_url(self) -> str:
        return f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
    
    # MongoDB
    mongodb_host: str = "localhost"
    mongodb_port: int = 27017
    mongodb_database: str = "acm_platform"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### 2. 统一响应 (response.py)

```python
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel
from datetime import datetime

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None
    timestamp: int = None
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.timestamp is None:
            self.timestamp = int(datetime.now().timestamp() * 1000)
    
    @classmethod
    def success(cls, data: Any = None, message: str = "success"):
        return cls(code=200, message=message, data=data)
    
    @classmethod
    def fail(cls, code: int = 400, message: str = "error"):
        return cls(code=code, message=message)
```

### 3. 异常处理 (exceptions.py)

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

class BusinessException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

class ErrorCode:
    # 通用 1xxxx
    PARAM_ERROR = (10001, "参数错误")
    UNAUTHORIZED = (10002, "未授权，请先登录")
    FORBIDDEN = (10003, "无权限访问")
    NOT_FOUND = (10004, "资源不存在")
    
    # 用户 2xxxx
    USER_NOT_FOUND = (20001, "用户不存在")
    USER_EXISTS = (20002, "用户已存在")
    PASSWORD_ERROR = (20003, "密码错误")
    
    # 积分 4xxxx
    POINTS_NOT_ENOUGH = (40001, "积分不足")

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        logger.warning(f"[BUSINESS_ERROR] {exc.code}: {exc.message}")
        return JSONResponse(
            status_code=200,
            content={"code": exc.code, "message": exc.message, "data": None}
        )
```

### 4. Service层示例 (user_service.py)

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.models.mysql.user import User
from app.api.v1.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import BusinessException, ErrorCode

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user_in: UserCreate) -> User:
        # 检查邮箱是否存在
        existing = await self.get_by_email(user_in.email)
        if existing:
            raise BusinessException(*ErrorCode.USER_EXISTS)
        
        # 创建用户
        user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            nickname=user_in.nickname or user_in.email.split("@")[0],
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        
        logger.info(f"[USER][REGISTER] userId={user.id}, email={user.email}")
        return user
    
    async def authenticate(self, email: str, password: str) -> dict:
        user = await self.get_by_email(email)
        if not user:
            raise BusinessException(*ErrorCode.USER_NOT_FOUND)
        if not verify_password(password, user.hashed_password):
            raise BusinessException(*ErrorCode.PASSWORD_ERROR)
        
        access_token = create_access_token(str(user.id))
        logger.info(f"[USER][LOGIN] userId={user.id}")
        return {"user": user, "access_token": access_token}
    
    async def get_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
```

### 5. API端点示例 (user.py)

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.mysql import get_mysql_session
from app.api.deps import get_current_user
from app.api.v1.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.core.response import Response
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.post("/register", response_model=Response[UserResponse])
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_mysql_session),
):
    """用户注册"""
    service = UserService(db)
    user = await service.create_user(user_in)
    return Response.success(data=UserResponse.model_validate(user))

@router.post("/login", response_model=Response[TokenResponse])
async def login(
    login_in: UserLogin,
    db: AsyncSession = Depends(get_mysql_session),
):
    """用户登录"""
    service = UserService(db)
    result = await service.authenticate(login_in.email, login_in.password)
    return Response.success(data=TokenResponse(
        access_token=result["access_token"],
        user=UserResponse.model_validate(result["user"]),
    ))

@router.get("/me", response_model=Response[UserResponse])
async def get_me(current_user = Depends(get_current_user)):
    """获取当前用户"""
    return Response.success(data=UserResponse.model_validate(current_user))
```

### 6. 单元测试示例

```python
# tests/test_services/test_user_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.user_service import UserService
from app.api.v1.schemas.user import UserCreate
from app.core.exceptions import BusinessException, ErrorCode

class TestUserService:
    @pytest.fixture
    def mock_db(self):
        db = AsyncMock()
        db.add = MagicMock()
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        return db
    
    @pytest.fixture
    def service(self, mock_db):
        return UserService(mock_db)
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, service):
        """测试创建用户 - 成功"""
        user_in = UserCreate(email="test@example.com", password="password123")
        with patch.object(service, 'get_by_email', return_value=None):
            result = await service.create_user(user_in)
        assert result.email == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_create_user_email_exists(self, service):
        """测试创建用户 - 邮箱已存在"""
        user_in = UserCreate(email="existing@example.com", password="password123")
        with patch.object(service, 'get_by_email', return_value=MagicMock()):
            with pytest.raises(BusinessException) as exc_info:
                await service.create_user(user_in)
        assert exc_info.value.code == ErrorCode.USER_EXISTS[0]
```

---

## 🚨 重要提醒

### 开发流程检查清单

每次开发前检查：

```
☐ 是否在dev分支？
☐ 是否拉取了最新代码？
☐ Docker服务是否启动？
☐ 虚拟环境是否激活？
```

每次提交前检查：

```
☐ 单元测试是否全部通过？
☐ 代码覆盖率是否 > 80%？
☐ 是否有未处理的异常？
☐ 日志记录是否完整？
☐ 提交信息是否规范？
```

### 必须遵守的规则

1. **测试先行**: 每个Service必须有单元测试，覆盖率 > 80%
2. **Git规范**: 测试通过后才能提交，提交信息遵循规范
3. **日志记录**: 关键操作必须记录日志
4. **异常处理**: 使用BusinessException，不要直接raise Exception
5. **前端验证**: 使用uipro开发，必须在浏览器验证效果

### 常见问题解决

```bash
# MySQL连接失败
docker-compose -f docker/docker-compose.dev.yml restart mysql

# MongoDB连接失败
docker-compose -f docker/docker-compose.dev.yml restart mongodb

# 端口被占用
lsof -i :8000  # 查看占用进程
kill -9 <PID>  # 结束进程

# 依赖安装失败
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

---

## 📚 参考文档

| 文档 | 位置 | 说明 |
|------|------|------|
| 需求文档 | `docs/PRD-V4.md` | 完整产品需求 |
| 开发指南 | `docs/开发指南-V3.md` | 技术方案详情 |
| 任务清单 | `docs/任务清单-V3.md` | 完整任务列表 |
| API文档 | `http://localhost:8000/docs` | Swagger文档 |

---

## 🎯 当前任务

**请按以下顺序执行任务:**

1. 检查开发环境是否就绪
2. 查看当前Phase的待办任务
3. 按任务编号顺序开发
4. 每个模块完成后运行测试
5. 测试通过后提交到Git

**开始开发时，请告诉我你要开发哪个模块，我会提供详细指导。**

---

> 💡 **提示**: 如有疑问，请参阅 `docs/PRD-V4.md` 和 `docs/开发指南-V3.md`
