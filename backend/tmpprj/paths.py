from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent  # backend/tmpprj/（容器里是 /app/tmpprj）
BACKEND_DIR = PACKAGE_DIR.parent               # backend/（容器里是 /app）

FILES_DIR = BACKEND_DIR / "files"   # 上传落地目录（容器里是 /app/files，挂载自 ./backend/files）
STATIC_DIR = PACKAGE_DIR / "toor"   # /toor 静态挂载点
LOG_FILE = PACKAGE_DIR / "log.txt"
