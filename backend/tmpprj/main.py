from typing import Union
from fastapi import FastAPI,HTTPException,Response,Request,Form,Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
#from uuid import uuid4
from re import search
import datetime
from sqlalchemy.orm import Session

#import CORS
from tmpprj.databases import db
from tmpprj.databases.session import get_db
from tmpprj.security import hashPasswd
from tmpprj.security.token import tokenCk_Pattern, tokenCrt, tokenDis

from tmpprj.home import router as home_router
from tmpprj.video import router as video_router
from tmpprj.paths import LOG_FILE, STATIC_DIR


# 以前是 app.mount("/home", home_app) + home_app.mount("/video", video_app) 三层嵌套子应用，
# 后果是 /docs 只列出主应用那 9 条，/home/* 和 /home/video/* 全都看不见。
# 改成 APIRouter 后所有路由挂在同一个应用上，一份 /docs 就全了。
app = FastAPI()
app.include_router(home_router, prefix="/home")
app.include_router(video_router, prefix="/home/video")
# staticfiles 的 mount 只能在 app 上做，所以从 home.py 挪到了这里
app.mount("/home/toor", StaticFiles(directory=STATIC_DIR), name="toor")

class login(BaseModel):
    passwd: str=Form(...)
    usrname: str=Form(...)
class usrname(BaseModel):
    usrname: str=Form(...)

@app.post("/login")###############################
def create_item(body: login, response: Response, session: Session = Depends(get_db)):
    # 这里原来用 lock.acquire(blocking=False) 把并发卡成 1（忙就返回 503 并发锁），
    # 那是在给「模块级 Session 单例被所有请求共用」打补丁。
    # 现在每个请求一个 Session（见 databases/session.py），锁不需要了，
    # 并发交给数据库连接池（QueuePool, pool_size=5）。
    print(body.usrname)
    if(body.passwd=='' or body.usrname==''):
        return 401
    id= db.dbLogin(session, body.usrname, hashPasswd.hashPass(body.passwd))
    print('uid is: '+str(id))
    if(id>=0):###========登陆成功一半=========
        token=tokenCrt(session, body.usrname, id)
        print('====LOGIN=====')
        response.set_cookie(key = 'usr_status', value = str(id) ,samesite='strict',expires=18000)
        return {"Hello": 1, "id":id,"token":token , "set_cookie": datetime.datetime.now().isoformat(sep = ' ')}
    else:
        return HTTPException(
            status_code=401,
            detail="用户名或密码错误",
        )

@app.post("/checkTmpName")
def checkName(tmpName: usrname, session: Session = Depends(get_db)):
    return db.checkNameRep(session, tmpName.usrname)


@app.post("/registry")
def registry(reg: login, session: Session = Depends(get_db)):
    print(reg.usrname)
    if(reg.passwd=='' or reg.usrname=='' or len(reg.usrname)>15 or len(reg.passwd)>1000 or search('<.+?>|\n|\r',reg.usrname)!=None):##记得写waf
        print('xs')
        return -1
    if(db.checkNameRep(session, reg.usrname)==1):
        hashpasswd=hashPasswd.hashPass(reg.passwd)
        t = db.dbReg(session, reg.usrname,hashpasswd)
        print('result is',t)
        return t#成功=1 否则失败  -1=非法输入
    return -2 #用户名存在


@app.get("/ckToken")
def ckToken(request: Request, response: Response, session: Session = Depends(get_db)):
    # 原来是 hashPasswd.tokenCk(...) —— hashPasswd 里根本没有这个函数，
    # 而且读的 usr_token cookie 从来没被设置过，所以这个端点一直是 500。
    # 现在统一走和别的端点一样的 tokenCk_Pattern（token 放在请求头里）。
    res=tokenCk_Pattern(session, request, response)
    return {'result':res}

@app.get('/logout')
def logout(request: Request,response: Response, session: Session = Depends(get_db)):
    res=tokenCk_Pattern(session, request,response)
    if(res==0):
        return 0#没有token

    uid=res['id']
    print('注销的id:'+str(uid))
    res2=tokenDis(session, uid)
    if(res2==0):
        return 0
    print('成功')
    response.delete_cookie("usr_status")
    return {"status":'logout'}


    
@app.get("/")
def read_root():
    return "我是帅哥"

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

#    uvicorn tmpprj.main:app --reload --port 8001
@app.get("/test")
def read_root(q:str, session: Session = Depends(get_db)):
    db.get_user_by_name(session, q)
    return q

@app.get("/getp")
def get(a:str,b:str,a1:str,b1:str,n:str):
    print(a)
    with open(LOG_FILE, 'a') as f:
        f.write('a:'+a+' b:'+b+' a1:'+a1+' b1:'+b1+' n:'+n+'\n')
