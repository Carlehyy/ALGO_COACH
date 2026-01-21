#!/bin/bash
# ============================================================
# ACM算法学习平台 - 前端启动脚本
# ============================================================

set -e  # 遇到错误立即退出

echo "🎨 启动 ACM算法学习平台 - 前端服务"
echo "======================================"

# 进入前端目录
cd "$(dirname "$0")"

# 检查 Node.js 版本
echo "📋 检查 Node.js 版本..."
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js 18+"
    echo "   下载地址: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js 版本: $NODE_VERSION"

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo "❌ 错误: 未找到 npm"
    exit 1
fi

NPM_VERSION=$(npm --version)
echo "✅ npm 版本: $NPM_VERSION"

# 检查依赖
echo "📋 检查依赖..."
if [ ! -d "node_modules" ]; then
    echo "⚠️  依赖未安装，正在安装..."
    npm install
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖已安装"
fi

# 检查 .env.local 文件
echo "📋 检查环境变量配置..."
if [ ! -f ".env.local" ]; then
    if [ -f ".env.example" ]; then
        echo "⚠️  .env.local 文件不存在，从 .env.example 复制..."
        cp .env.example .env.local
        echo "✅ .env.local 创建完成"
    else
        echo "⚠️  .env.example 文件不存在，创建默认配置..."
        cat > .env.local << EOF
# 前端环境变量配置

# API 地址（开发环境通过 Vite 代理到后端）
VITE_API_BASE_URL=/api/v1

# 后端 API 地址（用于直接访问，非代理模式）
# VITE_API_URL=http://localhost:8000
EOF
        echo "✅ .env.local 创建完成"
    fi
else
    echo "✅ .env.local 文件存在"
fi

# 启动开发服务器
echo ""
echo "======================================"
echo "🚀 启动 Vite 开发服务器..."
echo "======================================"
echo ""
echo "📍 前端地址: http://localhost:5173"
echo "📍 API代理: /api -> http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动 Vite
npm run dev
