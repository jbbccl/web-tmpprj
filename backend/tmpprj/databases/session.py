"""
以前是模块级单例被所有请求共用。SQLAlchemy 的
Session 不是线程安全的，两个请求同时进来就会共用同一个 Session

改成依赖注入后：每次请求现开一个 Session，用完自动关；Lock 就不需要了。
"""
from typing import Iterator

from sqlalchemy.orm import Session

from tmpprj.databases.db_info import SessionLocal


def get_db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session
