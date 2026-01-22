#!/bin/bash
# ============================================================
# ACM算法学习平台 - 极简启动脚本
# 无需任何外部数据库，使用 SQLite + 文件存储
# 适用于快速体验和测试
# ============================================================

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
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

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

print_header "🚀 ACM算法学习平台 - 极简模式（无外部数据库）"

print_warning "此模式使用以下替代方案："
print_warning "  - SQLite 替代 MySQL"
print_warning "  - 文件存储替代 MongoDB"
print_warning "  - 内存缓存替代 Redis"
print_warning "  - Mock AI 响应"
print_info "适合快速体验和开发测试"

echo ""
read -p "是否继续？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

# ============================================================
# 创建简化配置
# ============================================================

print_header "📝 创建简化配置"

cd "$PROJECT_ROOT/backend"

# 创建简化的 .env 文件
print_info "创建简化配置文件..."
cat > .env << 'EOF'
# ACM算法学习平台 - 简化配置（无需外部数据库）

APP_NAME=acm-learning-platform
APP_ENV=development
APP_DEBUG=true
APP_SECRET_KEY=dev-secret-key-change-in-production

# 使用 SQLite
SQLITE_URL=sqlite:///./acm_platform.db

# 禁用 MongoDB（使用文件存储）
MONGODB_DISABLED=true
FILE_STORAGE_PATH=./data/storage

# 禁用 Redis（使用内存缓存）
REDIS_DISABLED=true

# JWT 配置
JWT_SECRET_KEY=dev-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# 使用 Mock AI
USE_MOCK_AI=true

# CORS 配置
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# 积分配置
COACH_POINTS_PER_MESSAGE=10
NEW_USER_BONUS_POINTS=100
EOF

print_success "配置文件创建完成"

# 创建数据目录
mkdir -p data/storage logs

# ============================================================
# 后端启动
# ============================================================

print_header "🔧 启动后端"

# Python 检测
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

# 虚拟环境
if [ ! -d "venv" ]; then
    print_info "创建虚拟环境..."
    $PYTHON_CMD -m venv venv
fi

# 激活虚拟环境
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
fi

# 安装依赖
if ! $PYTHON_CMD -c "import fastapi" &> /dev/null; then
    print_info "安装依赖（首次运行需要几分钟）..."
    $PYTHON_CMD -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org

    # Termux SSL 修复：更新证书或使用可信主机
    print_info "修复 SSL 连接..."
    if command -v apt &> /dev/null; then
        apt update -qq && apt install -y ca-certificates -qq 2>/dev/null || true
    fi

    pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --default-timeout=100
    print_success "依赖安装完成"
fi

# 创建 SQLite 数据库
print_info "初始化数据库..."
if [ ! -f "acm_platform.db" ]; then
    $PYTHON_CMD -c "
from app.infrastructure.database.sqlite import init_sqlite
from alembic.config import Config
from alembic import command

# 初始化 SQLite
init_sqlite()

# 运行迁移
config = Config('alembic.ini')
command.upgrade(config, 'head')
print('SQLite 数据库初始化完成')
" 2>/dev/null || print_warning "数据库初始化跳过（请手动运行 alembic upgrade head）"
else
    print_success "数据库已存在"
fi

# 启动后端
print_info "启动后端服务..."
echo ""
echo -e "${GREEN}======================================"
echo "  后端服务已启动"
echo "======================================${NC}"
echo ""
echo "📍 API 地址: ${GREEN}http://localhost:8000${NC}"
echo "📍 API 文档: ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo "📝 使用的数据:"
echo "   - SQLite: backend/acm_platform.db"
echo "   - 文件存储: backend/data/storage/"
echo ""

# 后台启动后端
nohup $PYTHON_CMD -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "$PROJECT_ROOT/.backend.pid"
print_success "后端服务已启动 (PID: $BACKEND_PID)"

# 等待后端启动
print_info "等待后端服务启动..."
sleep 5

# 检查后端是否启动成功
if curl -s http://localhost:8000/health > /dev/null 2>&1 || curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    print_success "后端服务启动成功"
else
    print_warning "后端服务可能未正常启动，请查看日志: tail -f backend/logs/backend.log"
fi

# ============================================================
# 前端启动
# ============================================================

print_header "🎨 启动前端"

cd "$PROJECT_ROOT/frontend"

# Node.js 检测
if ! command -v node &> /dev/null; then
    print_error "未找到 Node.js，请先安装 Node.js 18+"
    exit 1
fi

NODE_VERSION=$(node --version)
print_success "Node.js: $NODE_VERSION"

# 安装依赖
if [ ! -d "node_modules" ]; then
    print_info "安装前端依赖（首次运行需要几分钟）..."
    npm install
    print_success "依赖安装完成"
fi

# 配置 .env.local
if [ ! -f ".env.local" ]; then
    cat > .env.local << 'EOF'
# 前端环境变量配置
VITE_API_BASE_URL=/api/v1
VITE_APP_TITLE=ACM算法学习平台
EOF
fi

# 启动前端
print_info "启动前端服务..."
echo ""
echo -e "${GREEN}======================================"
echo "  前端服务已启动"
echo "======================================${NC}"
echo ""
echo "📍 前端地址: ${GREEN}http://localhost:5173${NC}"
echo "📍 管理后台: ${GREEN}http://localhost:5173/admin/dashboard${NC}"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

npm run dev

# 清理：前端停止时停止后端
print_info "停止后端服务..."
if [ -f "$PROJECT_ROOT/.backend.pid" ]; then
    BACKEND_PID=$(cat "$PROJECT_ROOT/.backend.pid")
    kill $BACKEND_PID 2>/dev/null || true
    rm -f "$PROJECT_ROOT/.backend.pid"
    print_success "后端服务已停止"
fi
