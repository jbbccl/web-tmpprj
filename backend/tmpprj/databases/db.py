
# 只在“直接运行本文件”时（IDE 右键 Run / python -m tmpprj.databases.db）把包根目录
# 加进搜索路径。用 __file__ 定位，不依赖当前工作目录；被 import 时这段不执行。
if __name__ == "__main__":
    import pathlib
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from sqlalchemy import Column, DateTime, Integer, String, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from tmpprj.databases.db_info import Base, engine


class usrs(Base):
    __tablename__ = "usrs"
    id = Column(Integer, primary_key=True, index=True)
    # Column就类似django里的Table.objects
    # 里面放字段，字段必须在上面先导入
    name = Column(String(20), unique=True)
    passwd = Column(String(256))
    data = Column(DateTime, default=None)
    sess = Column(String(256), default=None, unique=True)
    bak = Column(String(32), default=None)


# ↓ 这些函数不再自己 SessionLocal()，而是收一个由 FastAPI 注入进来的 session。
#   原因见 tmpprj/databases/session.py。
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
        # 这里必须 rollback：session 现在是整个请求共用的，
        # 失败后不清理，同请求里后续拿它做任何事都会抛 PendingRollbackError。
        session.rollback()
        return 0


def dbLogin(session: Session, name, hashpasswd):
    # 这里收的是「已经 hash 过的密码」：hash 属于安全层(security)的事，
    # 数据层不该管，这样 databases 也就不必反向依赖 security 了。
    print('==========++++++++===========')
    q_user = session.query(usrs).filter(and_(usrs.name == name, usrs.passwd == hashpasswd)).first()
    if q_user is None:
        print('查无此人')
        return -1
    print(q_user.id)
    return q_user.id


def dbSessCrt(session: Session, name, id, sess_uuid):
    try:
        res = session.query(usrs).filter(and_(usrs.name == name, usrs.id == id)).update({"sess": sess_uuid})
        session.commit()
        print('ADD SESSION: ', end='')
        print(res)
        return res
    except Exception:
        session.rollback()
        return 0


def dbSessFin(session: Session, id):
    try:
        res = session.query(usrs.sess).filter(usrs.id == id).first()
        if res[0] is None:
            return 'sess_error'
        return res[0]
    except Exception:
        return 'sess_error'


def dbSessDis(session: Session, id):
    try:
        res = session.query(usrs).filter(and_(usrs.id == id)).update({"sess": None})
        print(res)
        session.commit()
        return 1
    except Exception:
        session.rollback()
        return 0


def get_user_by_name(session: Session, uname):
    return session.query(usrs).filter(usrs.name == uname).first()


# 调试用（注意这些函数现在都要传 session）：
# from tmpprj.databases.db_info import SessionLocal
# with SessionLocal() as s:
#     print(get_user_by_name(s, '111'))
#     print(dbSessFin(s, 3))
