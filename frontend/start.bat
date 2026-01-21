@echo off
REM ============================================================
REM ACM算法学习平台 - 前端启动脚本 (Windows)
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ======================================
echo   ACM算法学习平台 - 前端服务
echo ======================================
echo.

REM 进入前端目录
cd /d "%~dp0"

REM 检查 Node.js
echo [检查] Node.js...
where node >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js，请先安装 Node.js 18+
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo [成功] Node.js 版本: %NODE_VERSION%

REM 检查 npm
echo [检查] npm...
where npm >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 npm
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i
echo [成功] npm 版本: %NPM_VERSION%

REM 检查依赖
echo [检查] 依赖...
if not exist "node_modules\" (
    echo [警告] 依赖未安装，正在安装...
    call npm install
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
    echo [成功] 依赖安装完成
) else (
    echo [成功] 依赖已安装
)

REM 检查 .env.local
echo [检查] 环境变量配置...
if not exist ".env.local" (
    if exist ".env.example" (
        echo [警告] .env.local 不存在，从 .env.example 复制...
        copy .env.example .env.local >nul
        echo [成功] .env.local 创建完成
    ) else (
        echo [警告] .env.example 不存在，创建默认配置...
        (
            echo # 前端环境变量配置
            echo.
            echo # API 地址（开发环境通过 Vite 代理到后端）
            echo VITE_API_BASE_URL=/api/v1
        ) > .env.local
        echo [成功] .env.local 创建完成
    )
) else (
    echo [成功] .env.local 文件存在
)

REM 启动开发服务器
echo.
echo ======================================
echo   启动 Vite 开发服务器...
echo ======================================
echo.
echo   前端地址: http://localhost:5173
echo   API代理: /api -^> http://localhost:8000
echo.
echo   按 Ctrl+C 停止服务
echo.

call npm run dev

pause
