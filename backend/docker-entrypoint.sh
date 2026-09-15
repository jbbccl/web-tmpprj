#!/bin/sh
# 后端容器入口：准备依赖 -> 等数据库 -> 起 uvicorn
#
# 依赖装在 /app/.venv，而 /app 是宿主机 ./backend 挂进来的，
# 所以宿主机上能看到 ./backend/.venv/lib/python3.11/site-packages，
# VSCodium 的 basedpyright 就能解析 fastapi / jwt 这些包。
set -e

VENV=/app/.venv

if [ ! -x "$VENV/bin/uvicorn" ]; then
  echo "[entrypoint] 首次启动：创建 venv 并安装依赖（改动 requirements.txt 后删掉 backend/.venv 即可重装）"
  python -m venv "$VENV"
  "$VENV/bin/pip" install --no-cache-dir --upgrade pip
  "$VENV/bin/pip" install --no-cache-dir -r /app/requirements.txt
  echo "[entrypoint] 依赖安装完成"
fi

# 等 MariaDB 起来（首次启动要初始化数据目录，比较慢）
if [ -n "${SQL_ADDR:-}" ]; then
  i=0
  until "$VENV/bin/python" -c '
import os, pymysql, sys
try:
    pymysql.connect(
        host=os.environ["SQL_ADDR"],
        port=int(os.environ.get("SQL_PORT", "3306")),
        user=os.environ.get("SQL_USER", "dbtmp"),
        password=os.environ.get("SQL_PASSWORD", ""),
        connect_timeout=3,
    ).close()
except Exception:
    sys.exit(1)
' 2>/dev/null; do
    i=$((i + 1))
    if [ "$i" -ge 60 ]; then
      echo "[entrypoint] 等数据库超时（${SQL_ADDR}），退出" >&2
      exit 1
    fi
    echo "[entrypoint] 等待数据库 ${SQL_ADDR}:${SQL_PORT:-3306} ... ($i)"
    sleep 2
  done
  echo "[entrypoint] 数据库就绪"
fi

# CWD 必须是 /app/app：main.py 里 import 的是 databases / scret / home 这些顶层包
cd /app/app
exec "$VENV/bin/uvicorn" main:app --reload --host 0.0.0.0 --port 8001
