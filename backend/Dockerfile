# 后端镜像：只负责提供 Python + 依赖引导脚本。
# 三方依赖装在 ./backend/.venv（挂载卷内），见 docker-entrypoint.sh 的说明。
FROM docker.io/library/python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY . /app
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["/app/docker-entrypoint.sh"]
