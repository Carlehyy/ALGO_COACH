#!/bin/bash
# ============================================================
# ACM算法学习平台 - 快速开发启动
# 适用于本地开发环境
# ============================================================

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}======================================"
echo "  ACM算法学习平台 - 开发环境启动"
echo "======================================${NC}"
echo ""

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# 检查后端
if [ ! -d "$PROJECT_ROOT/backend/venv" ]; then
    echo -e "${YELLOW}⚠️  后端虚拟环境不存在，首次启动需要安装依赖${NC}"
fi

# 检查前端
if [ ! -d "$PROJECT_ROOT/frontend/node_modules" ]; then
    echo -e "${YELLOW}⚠️  前端依赖未安装，首次启动需要安装依赖${NC}"
fi

echo -e "${GREEN}🚀 启动开发环境...${NC}"
echo ""

# 在新终端窗口启动后端（如果支持）
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- bash -c "cd '$PROJECT_ROOT/backend' && ./start.sh" &
elif command -v xterm &> /dev/null; then
    xterm -e "cd '$PROJECT_ROOT/backend' && ./start.sh" &
else
    echo "提示：请在另一个终端运行: cd backend && ./start.sh"
    echo "      按任意键继续启动前端..."
    read
fi

# 等待后端启动
sleep 2

# 在当前终端启动前端
cd "$PROJECT_ROOT/frontend"
exec ./start.sh
