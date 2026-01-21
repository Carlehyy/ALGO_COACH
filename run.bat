@echo off
REM ============================================================
REM ACM算法学习平台 - Windows 统一启动脚本
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ======================================
echo   ACM算法学习平台 - 启动菜单
echo ======================================
echo.
echo   1. 完整模式 - 启动后端 + 前端
echo   2. 仅后端
echo   3. 仅前端
echo   4. 查看状态
echo   5. 环境检查
echo   6. 停止服务
echo   0. 退出
echo.

set /p choice="请选择 [1-6]: "

if "%choice%"=="1" goto FULL
if "%choice%"=="2" goto BACKEND
if "%choice%"=="3" goto FRONTEND
if "%choice%"=="4" goto STATUS
if "%choice%"=="5" goto CHECK
if "%choice%"=="6" goto STOP
if "%choice%"=="0" goto END
goto INVALID

:FULL
echo.
echo [启动] 完整模式...
start "ACM Backend" /D "%~dp0backend" backend\start.bat
timeout /t 3 /nobreak >nul
start "ACM Frontend" /D "%~dp0frontend" frontend\start.bat
echo.
echo [成功] 后端和前端已在独立窗口启动
goto END

:BACKEND
echo.
echo [启动] 仅后端...
cd backend
call start.bat
goto END

:FRONTEND
echo.
echo [启动] 仅前端...
cd frontend
call start.bat
goto END

:STATUS
echo.
echo ======================================
echo   服务状态
echo ======================================
echo.
echo 后端服务 (端口 8000):
netstat -ano | findstr ":8000.*LISTENING" && echo [运行中] || echo [未运行]
echo.
echo 前端服务 (端口 5173):
netstat -ano | findstr ":5173.*LISTENING" && echo [运行中] || echo [未运行]
echo.
goto END

:CHECK
echo.
echo ======================================
echo   环境检查
echo ======================================
echo.

echo Python:
where python >nul 2>&1 && (python --version && echo [OK]) || echo [未安装]
echo.

echo Node.js:
where node >nul 2>&1 && (node --version && echo [OK]) || echo [未安装]
echo.

echo MySQL:
where mysql >nul 2>&1 && echo [OK] || echo [未安装]
echo.

echo MongoDB:
where mongo >nul 2>&1 && echo [OK] || echo [未安装]
echo.

echo Redis:
where redis-cli >nul 2>&1 && echo [OK] || echo [未安装]
echo.

echo 配置文件:
if exist "backend\.env" (echo [OK] backend\.env) else (echo [缺失] backend\.env)
if exist "frontend\.env.local" (echo [OK] frontend\.env.local) else (echo [缺失] frontend\.env.local)
echo.

goto END

:STOP
echo.
echo [停止] 停止所有服务...
call stop.bat
goto END

:INVALID
echo.
echo [错误] 无效选项
goto END

:END
echo.
pause
