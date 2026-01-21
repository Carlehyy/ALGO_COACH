@echo off
REM ============================================================
REM ACM算法学习平台 - 后端启动脚本 (Windows)
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ======================================
echo   ACM算法学习平台 - 后端服务
echo ======================================
echo.

REM 进入后端目录
cd /d "%~dp0"

REM 检查 Python
echo [检查] Python...
where python >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.10+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [成功] Python 版本: %PYTHON_VERSION%

REM 检查虚拟环境
echo [检查] 虚拟环境...
if not exist "venv\" (
    echo [警告] 虚拟环境不存在，正在创建...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 虚拟环境创建失败
        pause
        exit /b 1
    )
    echo [成功] 虚拟环境创建完成
) else (
    echo [成功] 虚拟环境存在
)

REM 激活虚拟环境
echo [启动] 激活虚拟环境...
call venv\Scripts\activate.bat

REM 检查依赖
echo [检查] 依赖...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [警告] 依赖未安装，正在安装...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
    echo [成功] 依赖安装完成
) else (
    echo [成功] 依赖已安装
)

REM 检查 .env 文件
echo [检查] 环境变量配置...
if not exist ".env" (
    if exist ".env.example" (
        echo [警告] .env 不存在，从 .env.example 复制...
        copy .env.example .env >nul
        echo [警告] 请编辑 .env 文件，配置数据库连接和API密钥
        echo     notepad backend\.env
        echo.
        set /p CONFIRM="是否现在配置？(y/n): "
        if /i "!CONFIRM!"=="y" (
            notepad .env
        ) else (
            echo [提示] 请稍后手动配置 .env 文件
        )
    )
    echo [成功] .env 文件存在
) else (
    echo [成功] .env 文件存在
)

REM 创建日志目录
if not exist "logs\" mkdir logs

REM 可选：运行数据库迁移
echo.
set /p MIGRATE="是否运行数据库迁移？(y/n): "
if /i "!MIGRATE!"=="y" (
    echo [执行] 数据库迁移...
    alembic upgrade head
    if errorlevel 1 (
        echo [警告] 数据库迁移失败，请检查配置
    )
    echo [完成] 数据库迁移
)

REM 启动服务
echo.
echo ======================================
echo   启动 FastAPI 服务...
echo ======================================
echo.
echo   API 地址: http://localhost:8000
echo   API 文档: http://localhost:8000/docs
echo   ReDoc 文档: http://localhost:8000/redoc
echo.
echo   按 Ctrl+C 停止服务
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
