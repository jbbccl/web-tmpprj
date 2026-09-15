"""数据库的接线：引擎 / Session 工厂 / Base。

配置不再从这里读 —— 统一走 tmpprj.config.settings。

以前这个文件还顺手 re-export 了一大堆 fastapi / sqlalchemy 的名字
（`from sqlalchemy import Column, Integer, ...`），供别的模块 `import *` 时
"顺风车"用。现在各模块都显式 import 自己需要的东西，所以这里只留真正属于它的三样：
engine、SessionLocal、Base。
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from tmpprj.config import settings

engine = create_engine(
    settings.database_uri,
    poolclass=QueuePool,
    pool_size=5,
    pool_timeout=30,
    pool_recycle=1439,   # 防止断连
    echo=True,           # 打印所有 SQL，调试用；嫌吵就改成 False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


Base.to_dict = to_dict
