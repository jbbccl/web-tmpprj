# 前端镜像：node + vite dev server（开发用）。
# 源码通过 compose 的 bind mount 挂进来；node_modules 走独立卷，见 compose.yaml。
FROM docker.io/library/node:22-bookworm

WORKDIR /app

# 先装依赖，让镜像自带一份 node_modules（用于填充 node_modules 卷）
COPY package.json package-lock.json ./
RUN npm install --no-audit --no-fund

COPY . /app
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 5509

ENTRYPOINT ["/app/docker-entrypoint.sh"]
