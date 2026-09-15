if __name__ == "__main__":
    import pathlib
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from tmpprj.databases.db_info import Base, engine


class usrs(Base):
    __tablename__ = "usrs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)
    passwd = Column(String(256))
    data = Column(DateTime, default=None)
    bak = Column(String(32), default=None)
    # 原来的 sess 列（存这个用户的 session key）已经挪进 sessions 表：
    # 一列只能放一个会话，导致同一用户第二次登录会把上一次顶掉。


class sessions(Base):
    """一次登录 = 一行。这样同一用户可以有多个会话（多设备），
    注销也只需要删自己那一行，不会把别的设备一起踢下线。"""
    __tablename__ = "sessions"
    jti = Column(String(36), primary_key=True)   # 本次登录的唯一 id，同时写进 JWT 的 jti 声明
    user_id = Column(Integer, index=True)        # 对应 usrs.id（没建外键，和 videos.uper_id 保持一致）
    key = Column(String(64))                     # 用这把随机 key 签这个 token
    data = Column(DateTime, default=None)        # 创建时间
    exp = Column(DateTime, index=True)           # 过期时间，留给清理用


# 这些函数不再自己 SessionLocal()，而是收一个由 FastAPI 注入进来的 session。
# 每个请求共享session，如果在此函数内get session，则一个请求拿多个session
def checkNameRep(session: Session, tmpname):
    try:
        q_name = session.query(usrs).filter(usrs.name == tmpname).first()
        if q_name is None:
            print('ookk')
            return 1
        print('nono')
        return 0
    except SQLAlchemyError as e:
        print('ERROR==============================')
        print(e)
        session.rollback()
        return 0


def dbReg(session: Session, name, passwd):
    try:
        session.add(usrs(name=name, passwd=passwd))
        session.commit()
        print('注册成功')
        return 1
    except Exception:
        session.rollback()
        return 0


def dbLogin(session: Session, name, hashpasswd):
    print('==========++++++++===========')
    q_user = session.query(usrs).filter(and_(usrs.name == name, usrs.passwd == hashpasswd)).first()
    if q_user is None:
        print('查无此人')
        return -1
    print(q_user.id)
    return q_user.id


def sessionCrt(session: Session, jti, user_id, key, exp):
    """登记一次登录"""
    try:
        session.add(sessions(jti=jti, user_id=user_id, key=key,
                             data=datetime.utcnow(), exp=exp))
        session.commit()
        return 1
    except Exception:
        session.rollback()
        return 0


def sessionGet(session: Session, jti):
    """按 jti 取 (key, user_id)；没有就返回 None（已注销 / 伪造的 jti）"""
    try:
        row = session.query(sessions).filter(sessions.jti == jti).first()
    except Exception:
        return None
    if row is None:
        return None
    return row.key, row.user_id


def sessionDel(session: Session, jti):
    """只删这一次登录 —— 别的设备不受影响"""
    try:
        n = session.query(sessions).filter(sessions.jti == jti).delete()
        session.commit()
        return 1 if n else 0
    except Exception:
        session.rollback()
        return 0


def get_user_by_name(session: Session, uname):
    return session.query(usrs).filter(usrs.name == uname).first()


# 调试用（注意这些函数现在都要传 session）：
# from tmpprj.databases.db_info import SessionLocal
# with SessionLocal() as s:
#     print(get_user_by_name(s, '111'))
