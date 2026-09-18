# tmpprj

FastAPI 后端 + Vue/Vite 前端 + MariaDB。大文件分片上传练手项目。

## 配置

应用只从环境变量读配置 `tmpprj/config.py`
密码配置： `.env`

```bash
cp .env.example .env
```

## 用 Podman + compose 

```bash
podman-compose up -d
podman-compose logs -f backend
podman-compose down
podman-compose down -v 
```

```sh
uv venv --python 3.11 .venv
uv pip install -e backend

# 测试
.venv/bin/python backend/tests/smoke.py
```

## 数据库迁移（Alembic）

以前是 `Base.metadata.create_all`，数据库没就绪就会在 import 阶段直接崩，现在由 Alembic 管：

```bash
.venv/bin/python -m alembic current
.venv/bin/python -m alembic upgrade head 
.venv/bin/python -m alembic downgrade -1 
```

容器启动时会自动跑 `alembic upgrade head`（见 `docker-entrypoint.sh`）。

## 目录结构

```
backend/
├── pyproject.toml            依赖 + pytest/ruff 配置（唯一来源）
├── alembic.ini  migrations/  数据库迁移（env.py 从 tmpprj.config.settings 取连接串）
├── tmpprj/                   包（源码根是 backend/，所以 import 写 tmpprj.xxx）
│   ├── main.py               应用入口（uvicorn tmpprj.main:app）
│   ├── home.py  video.py     路由（APIRouter，统一挂在 main.py 上）
│   ├── config.py             配置唯一来源（pydantic-settings 的 Settings）
│   ├── paths.py              所有落地路径的唯一来源（不依赖 CWD）
│   ├── databases/            session.py(依赖注入) + db_info(引擎/Base) + 模型与查询
│   └── security/             hashPasswd(口令) + token(JWT)
├── tests/smoke.py            HTTP 端到端回归（12 项，纯标准库）
├── Dockerfile  docker-entrypoint.sh
└── files/                    上传落地目录（运行时数据）
```
