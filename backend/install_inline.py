import os
import sys
import subprocess

# 设置本地临时目录
tmp_dir = os.path.join(os.getcwd(), "tmp")
os.makedirs(tmp_dir, exist_ok=True)

os.environ['TMPDIR'] = tmp_dir
os.environ['TEMP'] = tmp_dir
os.environ['TMP'] = tmp_dir

print(f"使用临时目录: {tmp_dir}")
print("开始安装依赖...")

# 直接调用 pip 模块
result = subprocess.run([
    sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
], capture_output=True, text=True)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print(f"返回码: {result.returncode}")
