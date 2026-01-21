#!/bin/bash
# ============================================================
# ACM算法学习平台 - 统一启动脚本
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
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

print_header() {
    echo ""
    echo -e "${BLUE}======================================"
    echo "  $1"
    echo "======================================${NC}"
    echo ""
}

# 检查命令是否存在
check_command() {
    if command -v $1 &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# 检查端口是否被占用
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1
    else
        return 0
    fi
}

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

print_header "🚀 ACM算法学习平台 - 启动菜单"

echo "请选择启动模式："
echo ""
echo "  1) 🌐 完整模式 - 启动后端 + 前端"
echo "  2) 🔧 仅后端 - 启动 FastAPI 服务"
echo "  3) 🎨 仅前端 - 启动 Vue 前端"
echo "  4) 📊 查看状态 - 检查服务运行状态"
echo "  5) 🛠️  环境检查 - 检查依赖和配置"
echo "  6) 🧹 清理重启 - 停止所有服务并清理"
echo "  0) 退出"
echo ""
read -p "请输入选项 [1-6]: " choice

case $choice in
    1)
        print_header "🌐 完整模式 - 启动后端 + 前端"

        # 检查端口
        print_info "检查端口占用..."
        if ! check_port 8000; then
            print_warning "端口 8000 已被占用，请先停止后端服务"
        fi
        if ! check_port 5173; then
            print_warning "端口 5173 已被占用，请先停止前端服务"
        fi

        # 启动后端（后台）
        print_info "启动后端服务..."
        cd "$PROJECT_ROOT/backend"
        if [ -x "start.sh" ]; then
            ./start.sh &
            BACKEND_PID=$!
            echo $BACKEND_PID > .backend.pid
            print_success "后端服务已启动 (PID: $BACKEND_PID)"
        else
            print_error "后端启动脚本不存在或无执行权限"
            exit 1
        fi

        # 等待后端启动
        sleep 3

        # 启动前端
        print_info "启动前端服务..."
        cd "$PROJECT_ROOT/frontend"
        if [ -x "start.sh" ]; then
            ./start.sh
        else
            print_error "前端启动脚本不存在或无执行权限"
            exit 1
        fi
        ;;

    2)
        print_header "🔧 仅后端 - 启动 FastAPI 服务"

        if ! check_port 8000; then
            print_warning "端口 8000 已被占用"
            read -p "是否强制停止现有服务并重启？(y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                pkill -f "uvicorn app.main:app" || true
                sleep 1
            else
                exit 0
            fi
        fi

        cd "$PROJECT_ROOT/backend"
        if [ -x "start.sh" ]; then
            ./start.sh
        else
            print_error "后端启动脚本不存在"
            exit 1
        fi
        ;;

    3)
        print_header "🎨 仅前端 - 启动 Vue 前端"

        if ! check_port 5173; then
            print_warning "端口 5173 已被占用"
            read -p "是否强制停止现有服务并重启？(y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                pkill -f "vite" || true
                sleep 1
            else
                exit 0
            fi
        fi

        cd "$PROJECT_ROOT/frontend"
        if [ -x "start.sh" ]; then
            ./start.sh
        else
            print_error "前端启动脚本不存在"
            exit 1
        fi
        ;;

    4)
        print_header "📊 查看状态 - 检查服务运行状态"

        echo "后端服务 (端口 8000):"
        if check_port 8000; then
            print_warning "未运行"
        else
            print_success "运行中"
            lsof -i :8000 | grep LISTEN
        fi
        echo ""

        echo "前端服务 (端口 5173):"
        if check_port 5173; then
            print_warning "未运行"
        else
            print_success "运行中"
            lsof -i :5173 | grep LISTEN
        fi
        echo ""

        # 检查数据库
        echo "数据库服务:"
        if check_command mysql; then
            if mysql -h"${MYSQL_HOST:-localhost}" -u"${MYSQL_USER:-root}" -e "SELECT 1;" > /dev/null 2>&1; then
                print_success "MySQL 可连接"
            else
                print_warning "MySQL 无法连接"
            fi
        else
            print_warning "MySQL 客户端未安装"
        fi

        if check_command mongosh; then
            if mongosh --eval "db.stats()" > /dev/null 2>&1; then
                print_success "MongoDB 可连接"
            else
                print_warning "MongoDB 无法连接"
            fi
        elif check_command mongo; then
            if mongo --eval "db.stats()" > /dev/null 2>&1; then
                print_success "MongoDB 可连接"
            else
                print_warning "MongoDB 无法连接"
            fi
        else
            print_warning "MongoDB 客户端未安装"
        fi

        if check_command redis-cli; then
            if redis-cli ping > /dev/null 2>&1; then
                print_success "Redis 可连接"
            else
                print_warning "Redis 无法连接"
            fi
        else
            print_warning "Redis 客户端未安装"
        fi
        ;;

    5)
        print_header "🛠️  环境检查 - 检查依赖和配置"

        echo "检查系统依赖:"
        echo ""

        # Python
        echo -n "Python 3.10+: "
        if check_command python3.11 || check_command python3.10 || check_command python3; then
            print_success "$(python3 --version 2>&1)"
        else
            print_error "未安装"
        fi

        # Node.js
        echo -n "Node.js 18+: "
        if check_command node; then
            print_success "$(node --version)"
        else
            print_error "未安装"
        fi

        # MySQL
        echo -n "MySQL 客户端: "
        if check_command mysql; then
            print_success "已安装"
        else
            print_warning "未安装"
        fi

        # MongoDB
        echo -n "MongoDB 客户端: "
        if check_command mongosh || check_command mongo; then
            print_success "已安装"
        else
            print_warning "未安装"
        fi

        # Redis
        echo -n "Redis 客户端: "
        if check_command redis-cli; then
            print_success "已安装"
        else
            print_warning "未安装"
        fi

        # Docker
        echo -n "Docker: "
        if check_command docker; then
            print_success "$(docker --version | cut -d' ' -f3)"
        else
            print_warning "未安装"
        fi

        echo ""
        echo "检查配置文件:"
        echo ""

        # Backend .env
        echo -n "backend/.env: "
        if [ -f "$PROJECT_ROOT/backend/.env" ]; then
            print_success "存在"
        else
            print_warning "不存在 (将从 .env.example 复制)"
        fi

        # Frontend .env.local
        echo -n "frontend/.env.local: "
        if [ -f "$PROJECT_ROOT/frontend/.env.local" ]; then
            print_success "存在"
        else
            print_warning "不存在"
        fi

        # Backend venv
        echo -n "backend/venv: "
        if [ -d "$PROJECT_ROOT/backend/venv" ]; then
            print_success "存在"
        else
            print_warning "不存在"
        fi

        # Frontend node_modules
        echo -n "frontend/node_modules: "
        if [ -d "$PROJECT_ROOT/frontend/node_modules" ]; then
            print_success "存在"
        else
            print_warning "不存在"
        fi
        ;;

    6)
        print_header "🧹 清理重启 - 停止所有服务并清理"

        print_info "停止后端服务..."
        pkill -f "uvicorn app.main:app" || print_warning "后端服务未运行"
        rm -f "$PROJECT_ROOT/.backend.pid"

        print_info "停止前端服务..."
        pkill -f "vite" || print_warning "前端服务未运行"

        print_info "清理临时文件..."
        cd "$PROJECT_ROOT/backend"
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -type f -name "*.pyc" -delete 2>/dev/null || true

        print_success "清理完成"
        ;;

    0)
        echo "👋 再见！"
        exit 0
        ;;

    *)
        print_error "无效选项"
        exit 1
        ;;
esac
