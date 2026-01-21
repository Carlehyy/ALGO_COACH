# 🚀 快速启动指南

## 环境要求

### 必需
- **Python 3.10+** - [下载地址](https://www.python.org/downloads/)
- **Node.js 18+** - [下载地址](https://nodejs.org/)
- **MySQL 8.0+**
- **MongoDB 6.0+**
- **Redis 7+**

### 可选
- **Docker & Docker Compose** - 用于启动数据库服务

---

## 一键启动（推荐）

### Linux / macOS

```bash
# 进入项目根目录
cd acm-learning-platform

# 运行启动脚本
./start.sh
```

启动后会显示菜单：
- `1` - 完整模式（后端 + 前端）
- `2` - 仅后端
- `3` - 仅前端
- `4` - 查看状态
- `5` - 环境检查
- `6` - 清理重启

### Windows

双击运行：
- `start.bat` - 完整模式启动
- `stop.bat` - 停止所有服务

---

## 手动启动

### 1. 启动数据库服务

**使用 Docker（推荐）：**
```bash
cd docker
docker-compose -f docker-compose.dev.yml up -d
```

**或手动启动：**
- MySQL: `mysqld --console`
- MongoDB: `mongod`
- Redis: `redis-server`

### 2. 启动后端

```bash
cd backend

# 方式1：使用启动脚本
./start.sh

# 方式2：手动启动
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

访问：http://localhost:8000/docs

### 3. 启动前端

```bash
cd frontend

# 方式1：使用启动脚本
./start.sh  # Windows: start.bat

# 方式2：手动启动
npm install
npm run dev
```

访问：http://localhost:5173

---

## 配置说明

### 后端配置

编辑 `backend/.env`：

```bash
# 复制示例配置
cp backend/.env.example backend/.env

# 编辑配置（至少修改以下项）
vim backend/.env
```

**必须配置项：**
- `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`
- `MONGODB_HOST`, `MONGODB_DATABASE`
- `REDIS_HOST`
- `JWT_SECRET_KEY`（生产环境必须修改）
- `ANTHROPIC_API_KEY`（使用真实AI时需要）

### 前端配置

编辑 `frontend/.env.local`：

```bash
# 复制示例配置
cp frontend/.env.example frontend/.env.local

# 编辑配置
vim frontend/.env.local
```

---

## 数据库迁移

首次运行需要执行数据库迁移：

```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

---

## 开发工具访问

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端应用 | http://localhost:5173 | Vue应用 |
| 后端API | http://localhost:8000 | FastAPI |
| API文档 | http://localhost:8000/docs | Swagger UI |
| ReDoc文档 | http://localhost:8000/redoc | ReDoc |
| 管理后台 | http://localhost:5173/admin/dashboard | 后台管理 |

---

## 常见问题

### 1. 端口被占用

**Linux/Mac:**
```bash
# 查看占用端口的进程
lsof -i :8000  # 后端
lsof -i :5173  # 前端

# 停止进程
kill -9 <PID>
```

**Windows:**
```bash
# 查看占用端口的进程
netstat -ano | findstr :8000
tasklist | findstr <PID>

# 停止进程
taskkill /F /PID <PID>
```

### 2. Python 虚拟环境问题

```bash
# 删除旧虚拟环境
rm -rf backend/venv

# 重新创建
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 前端依赖问题

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 4. 数据库连接失败

1. 检查数据库服务是否启动
2. 检查 `.env` 配置是否正确
3. 确认防火墙未阻止连接

```bash
# 测试 MySQL 连接
mysql -h localhost -u root -p

# 测试 MongoDB 连接
mongosh

# 测试 Redis 连接
redis-cli ping
```

### 5. CORS 错误

检查 `backend/.env` 中的 `CORS_ORIGINS` 配置：

```bash
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 停止服务

### Linux / macOS
```bash
./stop.sh
```

### Windows
双击 `stop.bat`

### 手动停止
```bash
# 后端
pkill -f "uvicorn app.main:app"  # Linux/Mac
taskkill /F /IM python.exe        # Windows

# 前端
pkill -f "vite"                   # Linux/Mac
taskkill /F /IM node.exe          # Windows
```

---

## 开发模式 vs 生产模式

### 开发模式
- 后端：`uvicorn app.main:app --reload`
- 前端：`npm run dev`
- 支持 HMR（热模块替换）
- 详细日志输出

### 生产模式
- 后端：`uvicorn app.main:app --workers 4`
- 前端：`npm run build`
- 静态文件由 Nginx 提供服务
- 性能优化

---

## 下一步

启动成功后：

1. **注册账号**：访问 http://localhost:5173/user/register
2. **浏览笔记**：访问 http://localhost:5173/note
3. **查看知识图谱**：访问 http://localhost:5173/topic
4. **体验AI教练**：访问 http://localhost:5173/coach
5. **管理后台**：访问 http://localhost:5173/admin/dashboard

---

## 获取帮助

- 查看文档：`docs/` 目录
- 查看任务清单：`docs/任务清单.md`
- 提交问题：GitHub Issues
