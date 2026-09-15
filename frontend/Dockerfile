FROM docker.io/library/node:22-bookworm-slim

WORKDIR /app

COPY . /app
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 5509

ENTRYPOINT ["/app/docker-entrypoint.sh"]
