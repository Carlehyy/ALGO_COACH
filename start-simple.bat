@echo off
REM ============================================================
REM ACM算法学习平台 - 极简启动脚本
REM 无需任何外部数据库
REM Windows 版本
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ======================================
echo  ACM算法学习平台 - 极简模式
echo ======================================
echo.
echo 此模式使用以下替代方案：
echo   - SQLite 替代 MySQL
echo   - 文件存储替代 MongoDB
echo   - 内存缓存替代 Redis
echo   - Mock AI 响应
echo.
echo 适合快速体验和开发测试
echo.
pause

REM ============================================================
REM 创建简化配置
REM ============================================================

echo.
echo [配置] 创建简化配置...
cd /d "%~dp0backend"

REM 创建 .env 文件
(
    echo # ACM算法学习平台 - 简化配置（无外部数据库）
    echo.
    echo APP_NAME=acm-learning-platform
    echo APP_ENV=development
    echo APP_DEBUG=true
    echo APP_SECRET_KEY=dev-secret-key-change-in-production
    echo.
    echo # 使用 SQLite
    echo SQLITE_URL=sqlite:///./acm_platform.db
    echo.
    echo # 禁用 MongoDB（使用文件存储）
    echo MONGODB_DISABLED=true
    echo FILE_STORAGE_PATH=./data/storage
    echo.
    echo # 禁用 Redis（使用内存缓存）
    echo REDIS_DISABLED=true
    echo.
    echo # JWT 配置
    echo JWT_SECRET_KEY=dev-jwt-secret-key
    echo JWT_ALGORITHM=HS256
    echo JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
    echo.
    echo # 使用 Mock AI
    echo USE_MOCK_AI=true
    echo.
    echo # CORS 配置
    echo CORS_ORIGINS=http://localhost:5173,http://localhost:3000
    echo.
    echo # 日志配置
    echo LOG_LEVEL=INFO
    echo LOG_FILE=logs/app.log
    echo.
    echo # 积分配置
    echo COACH_POINTS_PER_MESSAGE=10
    echo NEW_USER_BONUS_POINTS=100
) > .env

REM 创建数据目录
if not exist "data\storage" mkdir data\storage
if not exist "logs" mkdir logs

echo [完成] 配置文件创建完成

REM ============================================================
REM 后端启动
REM ============================================================

echo.
echo ======================================
echo   启动后端服务
echo ======================================
echo.

REM Python 检测
where python >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python
    echo     请下载安装: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 虚拟环境
if not exist "venv\" (
    echo [创建] Python 虚拟环境...
    python -m venv venv
    echo [完成] 虚拟环境创建
)

echo [激活] 虚拟环境...
call venv\Scripts\activate.bat

REM 依赖
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [安装] Python 依赖（首次运行需要几分钟）...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo [完成] 依赖安装
)

REM 创建 SQLite 数据库
if not exist "acm_platform.db" (
    echo [初始化] 数据库...
    REM 注意：这里需要手动运行 alembic upgrade head
)

REM 启动后端
echo [启动] 后端服务...
echo.
echo   API 地址: http://localhost:8000
echo   API 文档: http://localhost:8000/docs
echo.
echo   使用数据: SQLite (backend\acm_platform.db)
echo.

start "ACM Backend" cmd /k "cd /d %CD% && venv\Scripts\activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM 等待后端启动
echo [等待] 后端服务启动...
timeout /t 5 /nobreak >nul

REM ============================================================
REM 前端启动
REM ============================================================

echo.
echo ======================================
echo   启动前端服务
echo ======================================
echo.

cd /d "%~dp0frontend"

REM Node.js 检测
where node >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js
    echo     请下载安装: https://nodejs.org/
    pause
    exit /b 1
)

REM 依赖
if not exist "node_modules\" (
    echo [安装] 前端依赖（首次运行需要几分钟）...
    call npm install
    echo [完成] 依赖安装
)

REM 配置
if not exist ".env.local" (
    (
        echo # 前端环境变量配置
        echo VITE_API_BASE_URL=/api/v1
        echo VITE_APP_TITLE=ACM算法学习平台
    ) > .env.local
)

REM 启动前端
echo [启动] 前端服务...
echo.
echo   前端地址: http://localhost:5173
echo   管理后台: http://localhost:5173/admin/dashboard
echo.

start "ACM Frontend" cmd /k "cd /d %CD% && npm run dev"

REM ============================================================
REM 完成
REM ============================================================

echo.
echo ======================================
echo   启动完成
echo ======================================
echo.
echo 后端和前端已在独立窗口启动
echo.
echo 访问地址:
echo   前端:     http://localhost:5173
echo   后端:     http://localhost:8000
echo   API文档:  http://localhost:8000/docs
echo   管理后台: http://localhost:5173/admin/dashboard
echo.
echo 关闭窗口即可停止服务
echo.
pause
