#!/bin/sh
# 前端容器入口：确保依赖存在后起 vite dev server
set -e

cd /app

# node_modules 是独立卷，第一次启动时是空的
if [ ! -d node_modules/vite ]; then
  echo "安装黑洞\n"
  npm ci --no-audit --no-fund
  npm cache clean --force
  echo "ok\n"
fi

exec npm run dev -- --host 0.0.0.0 --port 5509
