#!/bin/bash
# 完整启动脚本 - ACM算法学习平台

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${CYAN}======================================"
    echo "  $1"
    echo "======================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 进入backend目录
cd "$(dirname "$0")"
BACKEND_DIR="$(pwd)"

print_header "🚀 ACM算法学习平台 - 启动"

# 设置临时目录
mkdir -p tmp logs data/storage
export TMPDIR="$BACKEND_DIR/tmp"
export TEMP="$BACKEND_DIR/tmp"
export TMP="$BACKEND_DIR/tmp"

# 激活虚拟环境
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    print_error "虚拟环境不存在"
    exit 1
fi

# 检查依赖
print_info "检查依赖..."
if ! python -c "import fastapi" 2>/dev/null; then
    print_info "安装依赖中..."
    pip install --upgrade pip setuptools wheel --default-timeout=100 --quiet

    # 安装pydantic-core
    if [ -f "pydantic_core-2.41.5-cp312-cp312-musllinux_1_1_aarch64.whl" ]; then
        pip install ./pydantic_core-2.41.5-cp312-cp312-musllinux_1_1_aarch64.whl --no-deps --quiet
    fi

    # 安装其他依赖
    pip install fastapi uvicorn[standard] pydantic pydantic-settings sqlalchemy aiomysql alembic python-multipart email-validator python-jose --default-timeout=100 --quiet
    print_success "依赖安装完成"
fi

# 停止旧的后端进程
print_info "停止旧进程..."
pkill -f "uvicorn app.main:app" 2>/dev/null || true
sleep 2

# 启动后端
print_info "启动后端服务..."
nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > .backend.pid

# 等待后端启动
print_info "等待后端启动..."
for i in {1..10}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_success "后端启动成功"
        break
    fi
    if [ $i -eq 10 ]; then
        print_error "后端启动失败，查看日志:"
        tail -30 logs/backend.log
        exit 1
    fi
    sleep 1
done

print_header "📍 服务地址"
echo ""
echo "🔧 后端API:     ${GREEN}http://localhost:8000${NC}"
echo "📚 API文档:     ${GREEN}http://localhost:8000/docs${NC}"
echo "💚 健康检查:    ${GREEN}http://localhost:8000/health${NC}"
echo ""
echo "📝 后端日志:    tail -f logs/backend.log"
echo "🛑 停止后端:    kill $BACKEND_PID"
echo ""

# 启动前端
print_info "启动前端..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    print_info "安装前端依赖..."
    npm install --silent
fi

print_header "🎨 前端即将启动"
echo ""
echo "🌐 前端地址:    ${GREEN}http://localhost:5173${NC}"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

npm run dev

# 清理
print_info "停止后端服务..."
if [ -f "$BACKEND_DIR/.backend.pid" ]; then
    kill $(cat "$BACKEND_DIR/.backend.pid") 2>/dev/null || true
    rm -f "$BACKEND_DIR/.backend.pid"
fi
