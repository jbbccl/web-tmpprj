# tmpprj

FastAPI 后端 + Vue/Vite 前端 + MariaDB。大文件分片上传练手项目。

## 配置

**应用只从环境变量读配置**（`tmpprj/config.py`），不读任何文件。

环境变量从哪来：

| 怎么跑 | 谁把值放进去 |
| --- | --- |
| `podman-compose up` | compose 自己读仓库根的 `.env`，再按 `environment:` 注入容器 |
| 本机直跑后端 | 你自己导出：`set -a && . ./.env && set +a` |

所以还是要有一份仓库根的 `.env`（**已被 gitignore**）：

```bash
cp .env.example .env      # 然后按需改里面的值
```

`DB_PASSWORD` 和 `PASSWD_SALT` **在源码里没有默认值**，缺了会直接启动失败 ——
而不是悄悄用写死在源码里的口令。

⚠️ **改 `PASSWD_SALT` 会让库里所有已有账号登不上**：存的是用旧盐算出来的 hash，
换盐等于所有人的密码都不对了。

## 用 Podman + compose 

```bash
podman-compose up -d
podman-compose logs -f backend
podman-compose down
podman-compose down -v 
```

```sh
uv venv --python 3.11 .venv
uv pip install -e backend          # 依赖声明在 backend/pyproject.toml

# 跑后端（先把 .env 导出成环境变量，再跑；数据库连容器映射出来的 3306）
set -a && . ./.env && set +a
cd backend && ../.venv/bin/python -m uvicorn tmpprj.main:app --reload --port 8001

# 回归测试（重构期间每步都跑）
.venv/bin/python backend/tests/smoke.py
```

## 数据库迁移（Alembic）

建表**不再由代码在 import 时自动做**（以前是 `Base.metadata.create_all`，
数据库没就绪就会在 import 阶段直接崩，容器进重启循环），现在由 Alembic 管：

```bash
cd backend
../.venv/bin/python -m alembic current                        # 当前版本
../.venv/bin/python -m alembic upgrade head                   # 升到最新
../.venv/bin/python -m alembic revision --autogenerate -m "说明"  # 改了模型后生成迁移
../.venv/bin/python -m alembic downgrade -1                   # 回退一步
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

VSCodium 里 basedpyright 的解释器配置在 `.vscode/settings.json`（指向 `.venv`），
F5 的调试配置在 `.vscode/launch.json`。
