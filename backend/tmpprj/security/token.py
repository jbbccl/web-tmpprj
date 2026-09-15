import jwt
from datetime import datetime,timedelta
from uuid import uuid4
from fastapi import Depends,HTTPException,Request,Response
from sqlalchemy.orm import Session

if __name__ == "__main__":
    import pathlib
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from tmpprj.databases import db
from tmpprj.databases.session import get_db


def tokenCrt(session: Session, name, id):#此函数返回创建的token
    # 每次登录生成一个 jti + 一把随机 key，登记到 sessions 表（一行 = 一次登录），
    # 再用这把 key 签 token；注销就是删掉对应那一行。
    jti=str(uuid4())
    key=str(uuid4())
    exp=datetime.utcnow()+timedelta(hours=5)#==============TIME OUT++
    if(db.sessionCrt(session, jti, id, key, exp)==0):
        return 0
    try:
        payload={'exp':exp,
                'usrname':name,
                'id':id,
                'jti':jti}
        encoded_jwt = jwt.encode(payload, key, algorithm='HS256')
        print(encoded_jwt)
        return encoded_jwt
    except:
        return 0

def tokenCk(session: Session, encoded_jwt):
    try:
        claims=jwt.decode(encoded_jwt, algorithms=['HS256'], options={'verify_signature': False})
        jti=claims.get('jti')
        print('check token jti is:'+str(jti))

        row=db.sessionGet(session, jti)#查询这把 token 的 key
        if(row is None):#没有这个会话：已注销，或 jti 是编的
            print('session 不存在')
            return (0,'session 不存在')
        key,_uid=row

        deco=jwt.decode(encoded_jwt, key, algorithms=['HS256'])
        print(deco)
        return (1,deco)# res[0]==1代表成功
    except jwt.ExpiredSignatureError:
        print('JWT has expired.超时')
        return (0,'JWT has expired.超时')
    except jwt.InvalidTokenError:
        print('Invalid JWT.弃用')
        return (0,'Invalid JWT.弃用')

def tokenDis(session: Session, jti):
    return db.sessionDel(session, jti)#1成功0；只删这一次登录

def tokenCk_Pattern(session: Session, request: Request, response: Response):
    if('token' not in request.headers):
        response.delete_cookie("usr_status")
        return 0

    res=tokenCk(session, request.headers['token'])

    if(res[0]==0):
        response.delete_cookie("usr_status")
        return 0

    # jti 也带出去：注销要按它删"这一次登录"，而不是清掉这个用户的所有会话
    return {'usr_name':res[1]['usrname'],'id':res[1]['id'],'jti':res[1].get('jti')}


def current_user(request: Request, response: Response, session: Session = Depends(get_db)):
    """需要登录的端点 Depends 它就行，替代每个路由里重复的那几行：

        @router.get("/info")
        def info(uinfo: dict = Depends(current_user)):
            return {"usr_name": uinfo["usr_name"], "id": uinfo["id"]}

    注意顺序：request/response 没有默认值，必须排在 session 前面。
    校验不过直接 401（usr_status cookie 由 tokenCk_Pattern 顺手清掉）。
    """
    uinfo=tokenCk_Pattern(session, request, response)
    if(uinfo==0):
        raise HTTPException(status_code=401, detail="没有token")
    return uinfo
