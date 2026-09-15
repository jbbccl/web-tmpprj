#!/bin/sh
# 依赖装在 /app/.venv，/app 是宿主机 ./backend 挂进来的
set -e

VENV=/app/.venv

if [ ! -x "$VENV/bin/uvicorn" ]; then
  python -m venv "$VENV"
  "$VENV/bin/pip" install --no-cache-dir --upgrade pip
  # 依赖声明在 /app/pyproject.toml 里（原来的 requirements.txt 已并入）。
  # -e 是可编辑安装：只在 venv 里放一个指回 /app 的链接，源码始终取自
  # bind mount，不会被复制进 site-packages。
  "$VENV/bin/pip" install --no-cache-dir -e /app
  echo "依赖安装完成"
fi

mkdir -p /app/files

cd /app

# 建表交给 Alembic（以前是 import 期 Base.metadata.create_all ——
# 数据库没就绪时会在 import 阶段直接崩，容器就进重启循环）。
# compose 里 backend 是 depends_on: condition: service_healthy，所以走到这儿
# 数据库已经是可连接状态。
# 用 python -m alembic 而不是 alembic：venv 是用 pip install -e 建的，
# 命令行脚本不一定在，模块调用一定可用。
"$VENV/bin/python" -m alembic upgrade head

exec "$VENV/bin/uvicorn" tmpprj.main:app --reload --host 0.0.0.0 --port 8001
