from typing import Union
from fastapi import FastAPI,HTTPException,Response,Request,Form
from pydantic import BaseModel
from threading import Lock
#from uuid import uuid4
from re import search
import datetime
import sys
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys.path)
print(__file__[:-7])
sys.path.append(__file__[:-7])
print(sys.path)

#import CORS
from databases import db
from scret import hashPasswd,tocken

from home import home_app


lock=Lock()
lockLonin=Lock()
app = FastAPI()
app.mount("/home",home_app,name='home')

class login(BaseModel):
    passwd: str=Form(...)
    usrname: str=Form(...)
class usrname(BaseModel):
    usrname: str=Form(...)

@app.post("/login")###############################
def create_item(login: login, response: Response):
    acquired = lock.acquire(blocking=False)
    if acquired:
        try:
            #print(login.passwd)
            print(login.usrname)
            if(login.passwd=='' or login.usrname==''):
                return 401
            id= db.dbLogin(login.usrname,hashPasswd.hashPass(login.passwd))
            print('uid is: '+str(id))
            if(id>=0):###========登陆成功一半=========
                #uuid_key=uuid4()
                #f=dbSessCrt(login.usrname,login.passwd,uuid_key)
                #if(f==1):
                token=tocken.tokenCrt(login.usrname,id)#,uuid_key)
                print('====LOGIN=====')
                #response.set_cookie(key = 'usr_token', value = token ,httponly=True,samesite='strict')#,secure=True)
                response.set_cookie(key = 'usr_status', value = str(id) ,samesite='strict',expires=18000)
                return {"Hello": 1, "id":id,"token":token , "set_cookie": datetime.datetime.now().isoformat(sep = ' ')}
                '''else:
                    return HTTPException(
                            status_code=404,
                            detail="数据库繁忙",
                            )'''
            else:
                return HTTPException(
                    status_code=401,
                    detail="用户名或密码错误",
                )
        finally:
            print('====================无事发生===================')
            lock.release()
    else:
        print('====================无事发生==========并发锁=========')
        raise HTTPException(
            status_code=503,
            detail="service busy 并发=1",
        )

@app.post("/checkTmpName")
def checkName(tmpName: usrname):
    ckname=db.checkNameRep(tmpName.usrname)
    return ckname
    if(ckname==1): #可以注册
        return 1
    else:
        return 0


@app.post("/registry")
def create_item(reg: login):
    acquired = lock.acquire(blocking=False)
    if acquired:
        try:
            #print(reg.passwd)###
            print(reg.usrname)###
            if(reg.passwd=='' or reg.usrname=='' or len(reg.usrname)>15 or len(reg.passwd)>1000 or search('<.+?>|\n|\r',reg.usrname)!=None):##记得写waf
                print('xs')
                return -1
            #print('开查')
            ckname=0
            ckname=db.checkNameRep(reg.usrname)
            #print('查完')
            if(ckname==1):
                hashpasswd=hashPasswd.hashPass(reg.passwd)
                t = db.dbReg(reg.usrname,hashpasswd)
                print('result is',end='')
                print(t)
                return t#成功=1 否则失败  -1=非法输入 
            else:
                return -2 #用户名存在
        finally:
            print('====================无事发生===================')
            lock.release()
    else:
         print('====================无事发生==========并发锁=========')
         raise HTTPException(
            status_code=503,
            detail="service busy 并发=1",
        )
    

@app.get("/ckToken")
def ckToken(request: Request):
    #sesskey=dbSessFin(name)
    res=hashPasswd.tokenCk(request.cookies['usr_token'])#,sess_key)
    print(res)
    return {'result':res}

@app.get('/logout')
def logout(request: Request,response: Response):
    res=tocken.tokenCk_Pattern(request,response)
    if(res==0):
        return 0#没有token

    uid=res['id']
    print('注销的id:'+str(uid))
    res2=tocken.tokenDis(uid)
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

#    uvicorn main:app --reload --port 8001
@app.get("/test")
def read_root(q:str):
    db.查(q)
    return q

@app.get("/getp")
def get(a:str,b:str,a1:str,b1:str,n:str):
    print(a)
    with open('log.txt','a') as f:
        f.write('a:'+a+' b:'+b+' a1:'+a1+' b1:'+b1+' n:'+n+'\n')
