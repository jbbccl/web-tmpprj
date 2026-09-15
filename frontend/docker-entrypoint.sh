#!/bin/sh
# 前端容器入口：确保依赖存在后起 vite dev server
set -e

cd /app

# node_modules 是独立的卷，首次可能被镜像内容填充，也可能是空的
if [ ! -d node_modules/vite ]; then
  echo "[entrypoint] 安装前端依赖（改了 package.json 后删掉卷即可重装：podman volume rm tmpprj_frontend_node_modules）"
  npm install --no-audit --no-fund
fi

exec npm run dev -- --host 0.0.0.0 --port 5509
