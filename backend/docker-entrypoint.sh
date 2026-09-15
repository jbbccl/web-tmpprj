#!/bin/sh
# 依赖装在 /app/.venv，/app 是宿主机 ./backend 挂进来的
set -e

VENV=/app/.venv

if [ ! -x "$VENV/bin/uvicorn" ]; then
  python -m venv "$VENV"
  "$VENV/bin/pip" install --no-cache-dir --upgrade pip
  "$VENV/bin/pip" install --no-cache-dir -r /app/requirements.txt
  echo "依赖安装完成"
fi

mkdir -p /app/files

cd /app/app
exec "$VENV/bin/uvicorn" main:app --reload --host 0.0.0.0 --port 8001
