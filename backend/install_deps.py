#!/usr/bin/env python3
"""依赖安装脚本 - 绕过 shell 包装器"""
import os
import sys
import subprocess

# 设置本地临时目录
script_dir = os.path.dirname(os.path.abspath(__file__))
tmp_dir = os.path.join(script_dir, "tmp")
os.makedirs(tmp_dir, exist_ok=True)

os.environ['TMPDIR'] = tmp_dir
os.environ['TEMP'] = tmp_dir
os.environ['TMP'] = tmp_dir

print(f"使用临时目录: {tmp_dir}")

# 激活虚拟环境的 pip
venv_bin = os.path.join(script_dir, "venv", "bin")
pip_path = os.path.join(venv_bin, "pip")

print("=" * 50)
print("步骤 1: 升级 pip")
print("=" * 50)
subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)

print("\n" + "=" * 50)
print("步骤 2: 安装项目依赖")
print("=" * 50)
requirements_path = os.path.join(script_dir, "requirements.txt")
subprocess.run([pip_path, "install", "-r", requirements_path], check=True)

print("\n依赖安装完成！")
