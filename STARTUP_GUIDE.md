# 🚀 启动脚本使用指南

本项目提供了多种启动方式，适应不同的开发环境和需求。

---

## 📋 启动脚本概览

| 脚本 | 系统 | 说明 | 需求 |
|------|------|------|------|
| `start.sh` | Linux/Mac | 交互式菜单启动 | MySQL, MongoDB, Redis |
| `start-local.sh` | Linux/Mac | 本地数据库启动 | 本地已安装数据库 |
| `start-simple.sh` | Linux/Mac | 极简模式启动 | 无需任何数据库 |
| `start-dev.sh` | Linux/Mac | 快速开发启动 | MySQL, MongoDB, Redis |
| `stop.sh` | Linux/Mac | 停止所有服务 | - |
| `run.bat` | Windows | Windows 启动菜单 | 本地已安装数据库 |
| `start-local.bat` | Windows | Windows 本地启动 | 本地已安装数据库 |
| `start-simple.bat` | Windows | Windows 极简启动 | 无需任何数据库 |
| `stop.bat` | Windows | 停止所有服务 | - |

---

## 🎯 推荐启动方式

### 方式一：极简模式（推荐新手）

**适合场景：**
- 快速体验项目
- 本地没有安装数据库
- Termux/Android 环境

**Linux/Mac:**
```bash
./start-simple.sh
```

**Windows:**
```bash
start-simple.bat
```

**特点：**
- ✅ 无需安装任何数据库
- ✅ 使用 SQLite 存储数据
- ✅ 使用文件存储替代 MongoDB
- ✅ 使用内存缓存替代 Redis
- ✅ 使用 Mock AI 响应
- ⚠️ 不支持分布式部署
- ⚠️ 重启后数据可能丢失（SQLite 可保留）

---

### 方式二：本地数据库模式（推荐开发者）

**适合场景：**
- 本地已安装 MySQL/MongoDB/Redis
- 需要完整功能
- 开发调试

**前提条件：**
- MySQL 8.0+ 已启动
- MongoDB 6.0+ 已启动
- Redis 7+ 已启动

**Linux/Mac:**
```bash
./start-local.sh
```

**Windows:**
```bash
start-local.bat
```

**特点：**
- ✅ 完整功能支持
- ✅ 数据持久化
- ✅ 支持所有功能模块
- ⚠️ 需要手动启动数据库服务

---

### 方式三：Docker 完整模式（推荐生产环境）

**适合场景：**
- 需要完整环境
- 团队协作开发
- 生产环境部署

**前提条件：**
- Docker 已安装
- Docker Compose 已安装

**启动步骤：**
```bash
# 1. 启动数据库服务
cd docker
docker-compose -f docker-compose.dev.yml up -d

# 2. 启动应用
cd ..
./start.sh  # 选择选项 1
```

**特点：**
- ✅ 环境一致性
- ✅ 一键启动所有服务
- ✅ 易于团队协作
- ⚠️ 需要安装 Docker

---

## 📖 各脚本详细说明

### 1. start.sh - 交互式启动

**功能：**
- 显示启动菜单
- 支持选择性启动后端/前端
- 查看服务运行状态
- 环境检查
- 清理重启

**使用：**
```bash
./start.sh

# 菜单选项：
# 1 - 完整模式（后端 + 前端）
# 2 - 仅后端
# 3 - 仅前端
# 4 - 查看状态
# 5 - 环境检查
# 6 - 清理重启
```

---

### 2. start-local.sh - 本地数据库启动

**功能：**
- 检测本地数据库是否安装
- 自动配置数据库连接
- 启动后端和前端

**检测内容：**
- MySQL 连接测试
- MongoDB 连接测试
- Redis 连接测试

**使用：**
```bash
./start-local.sh
```

---

### 3. start-simple.sh - 极简模式启动

**功能：**
- 无需任何外部数据库
- 使用 SQLite
- 使用文件存储
- 内存缓存
- Mock AI

**使用：**
```bash
./start-simple.sh
```

**数据存储位置：**
- SQLite: `backend/acm_platform.db`
- 文件存储: `backend/data/storage/`

---

### 4. start-dev.sh - 快速开发启动

**功能：**
- 快速启动开发环境
- 后端后台运行
- 前端当前终端运行

**使用：**
```bash
./start-dev.sh
```

---

### 5. stop.sh / stop.bat - 停止服务

**功能：**
- 停止后端服务
- 停止前端服务
- 清理临时文件

**Linux/Mac:**
```bash
./stop.sh
```

**Windows:**
```bash
stop.bat
```

---

## 🔧 环境配置

### 后端配置文件

位置：`backend/.env`

**首次运行：**
```bash
# 从示例复制
cp backend/.env.example backend/.env

# 编辑配置
vim backend/.env
```

**必需配置项：**
```bash
# 数据库连接
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=acm_platform

# JWT 密钥（生产环境必须修改）
JWT_SECRET_KEY=your-secret-key

# Claude API（可选，使用 Mock 可不配置）
ANTHROPIC_API_KEY=your-api-key
```

### 前端配置文件

位置：`frontend/.env.local`

**首次运行：**
```bash
# 从示例复制
cp frontend/.env.example frontend/.env.local
```

---

## 🐛 常见问题

### 1. 端口被占用

**问题：** 端口 8000 或 5173 被占用

**解决：**
```bash
# Linux/Mac
lsof -i :8000  # 查看占用进程
kill -9 <PID>  # 停止进程

# Windows
netstat -ano | findstr :8000
taskkill /F /PID <PID>
```

### 2. Python 虚拟环境问题

**问题：** 虚拟环境无法激活或依赖安装失败

**解决：**
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 数据库连接失败

**问题：** 无法连接到 MySQL/MongoDB

**解决：**
```bash
# 检查数据库是否启动
mysql -h localhost -u root -p
mongosh
redis-cli ping

# 或使用极简模式（无需数据库）
./start-simple.sh
```

### 4. 前端依赖问题

**问题：** npm install 失败

**解决：**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 5. Termux 环境特殊问题

**问题：** Termux 下某些功能不可用

**解决：**
```bash
# Termux 环境推荐使用极简模式
./start-simple.sh

# 或安装必要包
pkg install python
```

---

## 📚 下一步

启动成功后：

1. **访问应用** - 打开浏览器访问 http://localhost:5173
2. **注册账号** - 创建第一个用户账号
3. **浏览功能** - 探索笔记、知识图谱、AI教练等功能
4. **查看API文档** - 访问 http://localhost:8000/docs
5. **管理后台** - 访问 http://localhost:5173/admin/dashboard

---

## 🎓 开发建议

### 首次开发推荐流程

1. 使用 `start-simple.sh` 快速体验
2. 熟悉代码结构后，安装本地数据库
3. 切换到 `start-local.sh` 进行完整开发
4. 生产部署时使用 Docker 模式

### 调试技巧

```bash
# 查看后端日志
tail -f backend/logs/app.log
tail -f backend/logs/error.log

# 查看前端编译错误
# 在浏览器控制台查看

# 测试 API
curl http://localhost:8000/health
```

---

## 💡 提示

- 所有启动脚本都会自动检查环境并安装依赖
- 首次运行会自动创建配置文件
- 极简模式适合快速体验，不建议用于生产
- 生产环境请使用 Docker 模式

---

## 📞 获取帮助

- 查看 `QUICKSTART.md` - 快速启动指南
- 查看 `README.md` - 项目文档
- 提交 Issue - 获取技术支持
