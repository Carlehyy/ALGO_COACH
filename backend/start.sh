#!/bin/bash
# ============================================================
# ACM算法学习平台 - 后端启动脚本
# ============================================================

set -e  # 遇到错误立即退出

echo "🚀 启动 ACM算法学习平台 - 后端服务"
echo "======================================"

# 进入后端目录
cd "$(dirname "$0")"

# 检查 Python 版本
echo "📋 检查 Python 版本..."
PYTHON_CMD=""
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD=python3.11
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD=python3.10
elif command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    echo "❌ 错误: 未找到 Python 3.10+，请先安装 Python"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Python 版本: $PYTHON_VERSION"

# 检查虚拟环境
echo "📋 检查虚拟环境..."
if [ ! -d "venv" ]; then
    echo "⚠️  虚拟环境不存在，正在创建..."
    $PYTHON_CMD -m venv venv
    echo "✅ 虚拟环境创建完成"
fi

# 激活虚拟环境
echo "📋 激活虚拟环境..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "❌ 错误: 无法找到虚拟环境激活脚本"
    exit 1
fi

# 检查依赖
echo "📋 检查依赖..."
if ! pip show fastapi > /dev/null 2>&1; then
    echo "⚠️  依赖未安装，正在安装..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖已安装"
fi

# 检查 .env 文件
echo "📋 检查环境变量配置..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "⚠️  .env 文件不存在，从 .env.example 复制..."
        cp .env.example .env
        echo "⚠️  请编辑 .env 文件，配置数据库连接和API密钥"
        echo "   vim backend/.env"
        echo ""
        read -p "是否现在配置？(y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ${EDITOR:-vim} .env
        else
            echo "⚠️  请稍后手动配置 .env 文件"
        fi
    else
        echo "❌ 错误: .env.example 文件不存在"
        exit 1
    fi
else
    echo "✅ .env 文件存在"
fi

# 创建日志目录
mkdir -p logs

# 检查数据库连接（可选）
echo "📋 检查数据库连接..."
if command -v mysql &> /dev/null; then
    if mysql -h"${MYSQL_HOST:-localhost}" -u"${MYSQL_USER:-root}" -p"${MYSQL_PASSWORD:-}" -e "USE ${MYSQL_DATABASE:-acm_platform};" > /dev/null 2>&1; then
        echo "✅ MySQL 连接成功"
    else
        echo "⚠️  MySQL 连接失败，请检查配置或启动MySQL服务"
    fi
else
    echo "⚠️  未检测到 MySQL 客户端，跳过连接检查"
fi

# 运行数据库迁移（可选）
echo ""
read -p "是否运行数据库迁移？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📋 运行数据库迁移..."
    alembic upgrade head
    echo "✅ 数据库迁移完成"
fi

# 启动服务
echo ""
echo "======================================"
echo "🚀 启动 FastAPI 服务..."
echo "======================================"
echo ""
echo "📍 API 地址: http://localhost:8000"
echo "📍 API 文档: http://localhost:8000/docs"
echo "📍 ReDoc 文档: http://localhost:8000/redoc"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动 Uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
