"""Alembic 运行环境。

两个关键点：

1. **连接串只有一个来源** —— `tmpprj.config.settings`，和运行时用的是同一份配置。
   所以本机调试和容器里跑迁移，指向的一定是同一个库（都是读 SQL_* 环境变量）。
   alembic.ini 里的 sqlalchemy.url 特意留空。

2. **target_metadata 必须包含全部模型** —— 模型分散在 db.py / home_db.py 里，
   autogenerate 靠 import 的副作用把它们注册到 Base.metadata 上。
   漏 import 任何一个模块，alembic 都会以为"这些表该删掉"，然后生成 DROP TABLE。
"""
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from tmpprj.config import settings
from tmpprj.databases.db_info import Base

# ↓ 只为触发模型注册（import 的副作用），不要删、不要"优化"掉
import tmpprj.databases.db as _db            # noqa: F401
import tmpprj.databases.home_db as _home_db  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 注意：这里**不要**写 config.set_main_option("sqlalchemy.url", settings.database_uri)。
# 转义后的密码里带 %XX（例如 ! @ # 会被转义），% 会被 configparser 当成插值语法直接报
# "invalid interpolation syntax"。所以下面自己 create_engine，绕开 ini。
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """不连库，只把 SQL 打出来（alembic upgrade --sql）。"""
    context.configure(
        url=settings.database_uri,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # 直接用 settings 建引擎（原因见上面那段注释）
    connectable = create_engine(settings.database_uri, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
