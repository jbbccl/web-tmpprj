
# 只在“直接运行本文件”时（IDE 右键 Run / python databases/db.py）把 app 根目录
# 加进搜索路径。用 __file__ 定位，不依赖当前工作目录；被 import 时这段不执行。
if __name__ == "__main__":
    import pathlib
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from databases.db_info import *



#Base = declarative_base()
class usrs(Base):
    __tablename__ = "usrs"
    id = Column(Integer, primary_key=True, index=True)
    # Column就类似django里的Table.objects
    # 里面放字段，字段必须在上面先导入
    name = Column(String(20),unique=True)
    passwd = Column(String(256))
    data = Column(DateTime,default=None)
    sess = Column(String(256),default=None,unique=True)
    bak = Column(String(32),default=None)

Base.metadata.create_all(bind=engine) #=============建表==============
usrSession = SessionLocal()#测试用

def checkNameRep(tmpname):
    with SessionLocal() as tmpsession:
        try:
            sql=text("")
            q_name = tmpsession.query(usrs).filter(usrs.name==tmpname).first()
            if(q_name==None):
                print('ookk')
                return 1
            else:
                print('nono')
                return 0
        except SQLAlchemyError as e:
            print('ERROR==============================')
            print(e)
            tmpsession.rollback()
            return 0

def dbReg(name,passwd):
    with SessionLocal() as reg_session:
        try:
            #stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
            #result = session.execute(stmt, {"y": 6})
            usrt=usrs(name=name,passwd=passwd)
            reg_session.add(usrt)
            reg_session.commit()
            print('注册成功')
            return 1
        except:
            return 0

def dbLogin(name,hashpasswd):
    # 这里收的是「已经 hash 过的密码」：hash 属于安全层(scret)的事，
    # 数据层不该管，这样 databases 也就不必反向依赖 scret 了。
    with SessionLocal() as tmpsession:
        print('==========++++++++===========')
        q_user = tmpsession.query(usrs).filter(and_(usrs.name==name,usrs.passwd==hashpasswd)).first()

        if(q_user == None):
            t=-1
            print('查无此人')
        else:
            print(q_user.id)
            t=q_user.id
        return (t)

def dbSessCrt(name,id,sess_uuid):
    with SessionLocal() as tmpsession:
        try:
            res=tmpsession.query(usrs).filter(and_(usrs.name == name,usrs.id== id)).update({"sess": sess_uuid})
            tmpsession.commit()
            print('ADD SESSION: ',end='')
            print(res)
            return res
        except:
            return 0


def dbSessFin(id):
    with SessionLocal() as tmpsession:
        try:
            res=tmpsession.query(usrs.sess).filter(usrs.id==id).first()
            if(res[0]==None):
                return 'sess_error'
            return res[0]
        except:
            return 'sess_error'
  
def dbSessDis(id):
    with SessionLocal() as tmpsession:
        try:
            res=tmpsession.query(usrs).filter(and_(usrs.id==id)).update({"sess": None})
            print(res)
            tmpsession.commit()
            return 1
        except:
            return 0

def 增():
    usr1=usrs(name='超级大便人',passwd='1111111')
    usrSession.add(usr1)
    usrSession.commit()

def 删():
    res=usrSession.query(usrs).filter(usrs.name=="超级大便人").all()
    #class_info = db_session.query(ClassTable).filter(ClassTable.name=="OldBoyS1").first()
    #db_session.query(Student).filter(Student.class_id == class_info.id).delete()
    usrSession.query(usrs).filter(usrs.id == res[3].id).delete()
    usrSession.commit()
    
def 查(uname):
    q_user = usrSession.query(usrs).filter(usrs.name==uname).first()
    return(q_user)
    #print(q_user.id)

def 改():
    res=usrSession.query(usrs).filter(usrs.name == "超级小便人").update({"passwd": usrs.passwd+'012'})
    print(res)
    usrSession.commit()
#查("""1"'\\u4e16 or 1=1#""")
#checkNameRep('超级大便人')
#checkNameRep('超级大便')
#注意：dbLogin 现在收的是「已经 hash 过」的值，调试时要自己先 hash
#from scret import hashPasswd
#dbLogin('111',hashPasswd.hashPass('111111'))
#res=dbReg('超级大便人',hashPasswd.hashPass('111111'))
#print(res)
#dbSessFin(3)