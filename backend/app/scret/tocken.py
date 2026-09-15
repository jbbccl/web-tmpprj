import jwt
from datetime import datetime,timedelta
from uuid import uuid4
from fastapi import Request,Response

'''========添加引用路径========'''
from sys import path
from os.path import abspath 
path.append(abspath('.'))
'''============================'''

from databases import db

def tokenCrt(name,id,key='default-039f-482f-860a-49538'):#此函数返回创建的token
    
    key=str(uuid4())
    t=db.dbSessCrt(name,id,key)
    if(t==0):
        return 0
    try:
        payload={'exp':datetime.utcnow()+timedelta(hours=5),#==============TIME OUT++
                'usrname':name,
                'id':id}
        encoded_jwt = jwt.encode(payload, key, algorithm='HS256')
        print(encoded_jwt)
        return encoded_jwt
    except:
        return 0

def tokenCk(encoded_jwt,key='default'):
    try:
        id=jwt.get_unverified_header(encoded_jwt.split('.')[1]+'.骗.偷袭')
        id=id['id']
        print('check token id is:'+str(id))
        key=db.dbSessFin(id)#查询key
        deco=jwt.decode(encoded_jwt, key, algorithms=['HS256'])
        print(deco)
        return (1,deco)# res[0]==1代表成功
    except jwt.ExpiredSignatureError:
        print('JWT has expired.超时')
        return (0,'JWT has expired.超时')
    except jwt.InvalidTokenError:
        print('Invalid JWT.弃用')
        return (0,'Invalid JWT.弃用')
    #except jwt.exceptions.ExpiredSignatureError:
        #print('Token time out')
def tokenDis(id):
    rst=db.dbSessDis(id)
    return rst #1成功0

def tokenCk_Pattern(request: Request,response: Response):                                     #这个判断没有作用
    if('token' not in request.headers):
        response.delete_cookie("usr_status")
        return 0
    
    res=tokenCk(request.headers['token'])#,sess_key)    '''token逻辑模板'''

    if(res[0]==0):#
        response.delete_cookie("usr_status")
        return 0
        
    return {'usr_name':res[1]['usrname'],'id':res[1]['id']}#token正确返回用户信息

#a=tokenCrt('超级db人','1')
#print(a)
#time.sleep(4)
#tokenCk(a)
#a=tokenCrt('aaabbcas')
#time.sleep(4)
#tokenCk(a)