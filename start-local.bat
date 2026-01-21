@echo off
REM ============================================================
REM ACM算法学习平台 - 本地启动脚本（无Docker）
REM Windows 版本
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ======================================
echo   ACM算法学习平台 - 本地启动
echo ======================================
echo.
echo 此脚本将：
echo   1. 检查本地环境
echo   2. 启动后端服务
echo   3. 启动前端服务
echo.
pause

REM ============================================================
REM 检查环境
REM ============================================================

echo.
echo [检查] 环境依赖...
echo.

REM Python
echo   Python...
where python >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python
    echo     请下载安装: https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo     [OK] %%i

REM Node.js
echo   Node.js...
where node >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js
    echo     请下载安装: https://nodejs.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do echo     [OK] %%i

REM 检查数据库
echo.
echo [检查] 数据库...
echo.

REM MySQL
where mysql >nul 2>&1
if errorlevel 1 (
    echo [警告] 未检测到 MySQL
    echo     将使用 SQLite 替代
    set USE_SQLITE=1
) else (
    echo [OK] MySQL 已安装
)

REM MongoDB
where mongo >nul 2>&1
if errorlevel 1 (
    echo [警告] 未检测到 MongoDB
    echo     将使用文件存储替代
) else (
    echo [OK] MongoDB 已安装
)

REM Redis
where redis-cli >nul 2>&1
if errorlevel 1 (
    echo [警告] 未检测到 Redis
    echo     将禁用缓存功能
) else (
    echo [OK] Redis 已安装
)

REM ============================================================
REM 后端启动
REM ============================================================

echo.
echo ======================================
echo   启动后端服务
echo ======================================
echo.

cd /d "%~dp0backend"

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
    echo [安装] Python 依赖...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo [完成] 依赖安装
)

REM 配置
if not exist ".env" (
    if exist ".env.example" (
        echo [创建] .env 配置文件...
        copy .env.example .env >nul
        echo [提示] 请编辑 backend\.env 配置数据库连接
        pause
    )
)

REM 日志目录
if not exist "logs\" mkdir logs

REM 启动后端
echo [启动] FastAPI 服务...
echo.
echo   API 地址: http://localhost:8000
echo   API 文档: http://localhost:8000/docs
echo.
echo 提示: 后端将在新窗口启动
echo.

start "ACM Backend" cmd /k "cd /d %CD% && venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM 等待后端启动
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

REM 依赖
if not exist "node_modules\" (
    echo [安装] 前端依赖...
    call npm install
    echo [完成] 依赖安装
)

REM 配置
if not exist ".env.local" (
    if exist ".env.example" (
        copy .env.example .env.local >nul
    )
)

REM 启动前端
echo [启动] Vite 开发服务器...
echo.
echo   前端地址: http://localhost:5173
echo.
echo 提示: 前端将在新窗口启动
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
echo 关闭窗口即可停止对应服务
echo.
pause
