#!/bin/bash
# ============================================================
# Termux 环境专用依赖安装脚本
# 解决 pydantic-core Rust 编译问题
# ============================================================

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 进入脚本所在目录
cd "$(dirname "$0")"
BACKEND_DIR="$(pwd)"

print_info "当前目录: $BACKEND_DIR"

# 检查 Python 版本
PYTHON_CMD=python3
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
PYTHON_FULL=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
print_info "Python 版本: $PYTHON_VERSION (完整: $PYTHON_FULL)"
ARCH=$($PYTHON_CMD -c "import platform; print(platform.machine())")
print_info "系统架构: $ARCH"

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    print_info "创建虚拟环境..."
    $PYTHON_CMD -m venv venv
    print_success "虚拟环境创建完成"
fi

# 激活虚拟环境
print_info "激活虚拟环境..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    print_error "无法找到虚拟环境激活脚本"
    exit 1
fi

# 设置临时目录
mkdir -p tmp
export TMPDIR="$BACKEND_DIR/tmp"
export TEMP="$BACKEND_DIR/tmp"
export TMP="$BACKEND_DIR/tmp"
print_info "临时目录: $TMPDIR"

# 升级 pip
print_info "升级 pip..."
pip install --upgrade pip setuptools wheel --default-timeout=100

# 方案 1: 尝试使用 --prefer-binary 和 --only-binary 优先安装预编译版本
print_info "尝试安装 pydantic-core (预编译版本)..."

# 设置 Termux 相关环境变量
export ANDROID_API_LEVEL=28
export CARGO_TARGET_AARCH64_LINUX_ANDROID_LINKER=aarch64-linux-android-clang

# 尝试安装，优先使用二进制包
if pip install pydantic-core==2.27.2 --prefer-binary --only-binary=:all: --default-timeout=100 2>/dev/null; then
    print_success "pydantic-core 安装成功 (预编译版本)"
else
    # 如果失败，尝试使用本地 wheel
    print_info "预编译版本不可用，尝试使用本地 wheel..."
    if [ -f "pydantic_core-2.27.2-cp312-cp312-linux_aarch64.whl" ]; then
        pip install ./pydantic_core-2.27.2-cp312-cp312-linux_aarch64.whl
        print_success "pydantic-core 安装成功 (本地 wheel)"
    elif [ -f "pydantic_core-2.41.5-cp312-cp312-musllinux_1_1_aarch64.whl" ]; then
        # musllinux wheel 通常兼容 Termux
        print_info "使用 musllinux wheel (可能兼容)..."
        pip install ./pydantic_core-2.41.5-cp312-cp312-musllinux_1_1_aarch64.whl --no-deps
        print_success "pydantic-core 安装成功 (musllinux wheel)"
        # 更新 requirements.txt 中的 pydantic 版本以匹配 pydantic-core 2.41.5
        sed -i 's/pydantic==2.10.5/pydantic==2.10.5/' requirements.txt
    else
        print_error "无法找到合适的 pydantic-core wheel"
        print_info "将尝试直接安装，可能需要很长时间..."

        # 最后尝试：直接安装，允许编译
        pip install pydantic-core==2.27.2 --default-timeout=100 || {
            print_error "pydantic-core 安装失败"
            print_info "您可以尝试:"
            print_info "  1. 手动下载 wheel 文件到此目录"
            print_info "  2. 或使用以下命令设置环境变量后重试:"
            print_info "     export ANDROID_API_LEVEL=28"
            print_info "     pip install pydantic-core"
            exit 1
        }
    fi
fi

# 安装其他依赖
print_info "安装其他依赖..."

# 创建临时 requirements 文件，排除已安装的包
cat requirements.txt | grep -v "^pydantic-core" | grep -v "^$" > requirements_temp.txt

pip install -r requirements_temp.txt --default-timeout=100

# 清理临时文件
rm -f requirements_temp.txt

print_success "所有依赖安装完成"

# 验证安装
print_info "验证安装..."
python3 -c "
import fastapi
import pydantic
import pydantic_core
import sqlalchemy

print('FastAPI:', fastapi.__version__)
print('Pydantic:', pydantic.__version__)
print('Pydantic Core:', pydantic_core.__version__)
print('SQLAlchemy:', sqlalchemy.__version__)
" && print_success "所有依赖验证通过" || print_error "部分依赖验证失败"

echo ""
echo -e "${GREEN}======================================"
echo "  依赖安装完成"
echo "======================================${NC}"
echo ""
