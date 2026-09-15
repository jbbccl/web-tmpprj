'''========添加引用路径========'''
from sys import path as syspath
from os.path import abspath 
syspath.append(abspath('.'))
'''============================'''
from fastapi import Depends,FastAPI
# 首先应该安装fastapi，sqlalchemy
from sqlalchemy import Boolean, Column, Integer, String,DateTime,desc
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool
from sqlalchemy import and_, or_,exists,not_,text

#SQL_ADDR='43.128.57.171'
#SQL_ADDR='192.168.86.131'
SQL_ADDR='localhost'
SQLALCHEMY_DATABASE_URI:str = 'mysql+pymysql://dbtmp:Dst123!%40#@'+SQL_ADDR+':3306/dbtmp'#192.168.86.131  43.128.57.171
engine = create_engine(SQLALCHEMY_DATABASE_URI,poolclass=QueuePool,
                       pool_size=5,
                       pool_timeout=30,
                       pool_recycle=1439,
                       echo=True)#防止断联
                       #pool_size=3,
                       #pool_pre_ping=True,max_overflow=5,pool_recycle=7200,pool_timeout=5)

SessionLocal = sessionmaker(autocommit=False,autoflush=True,bind=engine)

Base = declarative_base()
def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
Base.to_dict = to_dict