@echo off
REM ============================================================
REM ACM算法学习平台 - 停止服务脚本 (Windows)
REM ============================================================

echo.
echo ======================================
echo   停止 ACM算法学习平台服务
echo ======================================
echo.

REM 停止后端服务
echo [停止] 后端服务...
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "uvicorn" >nul
if not errorlevel 1 (
    taskkill /F /FI "WINDOWTITLE eq uvicorn*" >nul 2>&1
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" >nul 2>&1
    echo [成功] 后端服务已停止
) else (
    echo [提示] 后端服务未运行
)

REM 停止前端服务
echo [停止] 前端服务...
tasklist /FI "IMAGENAME eq node.exe" 2>nul | find /I "vite" >nul
if not errorlevel 1 (
    taskkill /F /FI "WINDOWTITLE eq *vite*" >nul 2>&1
    echo [成功] 前端服务已停止
) else (
    echo [提示] 前端服务未运行
)

echo.
echo ======================================
echo   所有服务已停止
echo ======================================
echo.

pause
