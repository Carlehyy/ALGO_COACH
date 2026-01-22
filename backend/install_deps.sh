#!/bin/bash
# 依赖安装脚本 - 使用本地临时目录

cd "$(dirname "$0")"

# 设置本地临时目录
mkdir -p tmp
export TMPDIR="$(pwd)/tmp"
export TEMP="$(pwd)/tmp"
export TMP="$(pwd)/tmp"

echo "使用临时目录: $TMPDIR"

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "开始安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt

echo "依赖安装完成！"
