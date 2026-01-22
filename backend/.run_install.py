#!/usr/bin/env python3
import os
import sys
import subprocess

tmp_dir = os.path.join(os.path.dirname(__file__), "tmp")
os.makedirs(tmp_dir, exist_ok=True)
os.environ['TMPDIR'] = tmp_dir
os.environ['TEMP'] = tmp_dir

result = subprocess.run([
    sys.executable, "-m", "pip", "install", "-r", "requirements.txt",
    "--no-cache-dir"
], cwd=os.path.dirname(__file__))

sys.exit(result.returncode)
