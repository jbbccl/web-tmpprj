from fastapi import Depends,FastAPI
# 首先应该安装fastapi，sqlalchemy
from sqlalchemy import Boolean, Column, Integer, String,DateTime,desc
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool
from sqlalchemy import and_, or_,exists,not_,text

'''========数据库连接信息========
默认值 = 原来本机跑的配置；容器里由 compose.yaml 用环境变量覆盖（SQL_ADDR=db）'''
from os import environ
from urllib.parse import quote_plus

SQL_ADDR = environ.get('SQL_ADDR', 'localhost')     #43.128.57.171  192.168.86.131
SQL_PORT = environ.get('SQL_PORT', '3306')
SQL_USER = environ.get('SQL_USER', 'dbtmp')
SQL_PASSWORD = environ.get('SQL_PASSWORD', 'Dst123!@#')  #明文，下面统一转义
SQL_DB = environ.get('SQL_DB', 'dbtmp')

_base = f"mysql+pymysql://{SQL_USER}:{quote_plus(SQL_PASSWORD)}"
SQLALCHEMY_DATABASE_URI: str = f"{_base}@{SQL_ADDR}:{SQL_PORT}/{SQL_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URI,poolclass=QueuePool,
                            pool_size=5,
                            pool_timeout=30,
                            pool_recycle=1439,
                            echo=True)#防止断联
                            #pool_size=3,
                            #pool_pre_ping=True,max_overflow=5,pool_recycle=7200,pool_timeout=5)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()
def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
Base.to_dict = to_dict