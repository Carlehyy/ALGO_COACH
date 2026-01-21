#!/bin/bash
# ============================================================
# ACM算法学习平台 - 停止服务脚本
# ============================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo "🛑 停止 ACM算法学习平台服务"
echo "======================================"

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 停止后端服务
echo ""
echo "停止后端服务..."
BACKEND_PID_FILE="$PROJECT_ROOT/.backend.pid"
if [ -f "$BACKEND_PID_FILE" ]; then
    BACKEND_PID=$(cat "$BACKEND_PID_FILE")
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        kill $BACKEND_PID
        print_success "后端服务已停止 (PID: $BACKEND_PID)"
    else
        print_warning "后端服务进程不存在"
    fi
    rm -f "$BACKEND_PID_FILE"
else
    # 尝试通过进程名查找
    if pkill -f "uvicorn app.main:app"; then
        print_success "后端服务已停止"
    else
        print_warning "后端服务未运行"
    fi
fi

# 停止前端服务
echo ""
echo "停止前端服务..."
if pkill -f "vite.*5173"; then
    print_success "前端服务已停止"
else
    print_warning "前端服务未运行"
fi

# 停止 Celery Worker（如果运行）
echo ""
echo "停止 Celery Worker..."
if pkill -f "celery.*worker"; then
    print_success "Celery Worker 已停止"
else
    print_warning "Celery Worker 未运行"
fi

echo ""
echo "======================================"
print_success "所有服务已停止"
