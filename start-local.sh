#!/bin/bash
# ============================================================
# ACM算法学习平台 - 本地启动脚本（无Docker）
# 适用于已经本地安装数据库或使用轻量级替代方案
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${CYAN}======================================"
    echo "  $1"
    echo "======================================${NC}"
    echo ""
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

print_header "🚀 ACM算法学习平台 - 本地启动（无Docker）"

# ============================================================
# 环境检测
# ============================================================

print_info "检测本地环境..."

# Python
PYTHON_CMD=""
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD=python3.11
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD=python3.10
elif command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    print_error "未找到 Python 3.10+，请先安装 Python"
    exit 1
fi
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
print_success "Python: $PYTHON_VERSION"

# Node.js
if ! command -v node &> /dev/null; then
    print_error "未找到 Node.js，请先安装 Node.js 18+"
    exit 1
fi
NODE_VERSION=$(node --version)
print_success "Node.js: $NODE_VERSION"

# ============================================================
# 数据库配置
# ============================================================

print_header "📊 数据库配置"

# 检查是否有可用的数据库
USE_MYSQL=false
USE_MONGODB=false
USE_REDIS=false

# MySQL 检测
if command -v mysql &> /dev/null || command -v mysqld &> /dev/null; then
    if mysql -h"${MYSQL_HOST:-localhost}" -u"${MYSQL_USER:-root}" -e "SELECT 1;" &> /dev/null 2>&1; then
        print_success "MySQL 可连接"
        USE_MYSQL=true
    else
        print_warning "MySQL 已安装但无法连接，可能需要启动服务"
        read -p "是否尝试使用 SQLite 替代 MySQL？(y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            USE_SQLITE=true
        fi
    fi
else
    print_warning "未检测到 MySQL"
    read -p "是否使用 SQLite 替代 MySQL？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        USE_SQLITE=true
    fi
fi

# MongoDB 检测
if command -v mongosh &> /dev/null || command -v mongo &> /dev/null; then
    if mongosh --eval "db.stats()" &> /dev/null 2>&1 || mongo --eval "db.stats()" &> /dev/null 2>&1; then
        print_success "MongoDB 可连接"
        USE_MONGODB=true
    else
        print_warning "MongoDB 已安装但无法连接，可能需要启动服务"
    fi
else
    print_warning "未检测到 MongoDB"
fi

# Redis 检测
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null 2>&1; then
        print_success "Redis 可连接"
        USE_REDIS=true
    else
        print_warning "Redis 已安装但无法连接，可能需要启动服务"
        print_info "将禁用需要 Redis 的功能（缓存、Celery）"
    fi
else
    print_warning "未检测到 Redis"
    print_info "将禁用需要 Redis 的功能（缓存、Celery）"
fi

# ============================================================
# 后端启动
# ============================================================

print_header "🔧 启动后端服务"

cd "$PROJECT_ROOT/backend"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    print_info "创建虚拟环境..."
    $PYTHON_CMD -m venv venv
    print_success "虚拟环境创建完成"
fi

# 激活虚拟环境
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    print_error "无法激活虚拟环境"
    exit 1
fi

# 安装依赖
if ! pip show fastapi &> /dev/null; then
    print_info "安装 Python 依赖..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "依赖安装完成"
fi

# 配置 .env 文件
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        print_info "创建 .env 配置文件..."
        cp .env.example .env

        # 根据检测结果调整配置
        if [ "$USE_SQLITE" = true ]; then
            print_info "配置使用 SQLite..."
            sed -i.bak 's|mysql_url=.*|sqlite_url=sqlite:///./acm_platform.db|' .env
        fi

        print_warning "请编辑 backend/.env 文件配置数据库连接"
        ${EDITOR:-vim} .env
    else
        print_error ".env.example 文件不存在"
        exit 1
    fi
fi

# 创建日志目录
mkdir -p logs

# 数据库迁移
print_info "运行数据库迁移..."
if alembic upgrade head 2>/dev/null; then
    print_success "数据库迁移完成"
else
    print_warning "数据库迁移失败（可能数据库未启动或配置错误）"
fi

# 启动后端
print_info "启动 FastAPI 服务..."
echo ""
echo -e "${GREEN}======================================"
echo "  后端服务已启动"
echo "======================================${NC}"
echo ""
echo "📍 API 地址: ${GREEN}http://localhost:8000${NC}"
echo "📍 API 文档: ${GREEN}http://localhost:8000/docs${NC}"
echo "📍 ReDoc 文档: ${GREEN}http://localhost:8000/redoc${NC}"
echo ""
echo "按 Ctrl+C 停止后端"
echo ""

# 保存后端 PID
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo $BACKEND_PID > "$PROJECT_ROOT/.backend.pid"
print_success "后端服务已启动 (PID: $BACKEND_PID)"

# ============================================================
# 前端启动
# ============================================================

# 等待后端启动
sleep 3

print_header "🎨 启动前端服务"

cd "$PROJECT_ROOT/frontend"

# 安装依赖
if [ ! -d "node_modules" ]; then
    print_info "安装前端依赖..."
    npm install
    print_success "依赖安装完成"
fi

# 配置 .env.local
if [ ! -f ".env.local" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env.local
    fi
fi

# 启动前端
print_info "启动 Vite 开发服务器..."
echo ""
echo -e "${GREEN}======================================"
echo "  前端服务已启动"
echo "======================================${NC}"
echo ""
echo "📍 前端地址: ${GREEN}http://localhost:5173${NC}"
echo ""
echo "按 Ctrl+C 停止前端"
echo ""

npm run dev
