from os.path import exists
import json
import time
# from typing import Union
from fastapi import APIRouter,HTTPException,Response,Request,UploadFile,File,Form,Depends
# from fastapi.responses import FileResponse

# from pydantic import BaseModel
from hashlib import md5 as hashlib_md5
from os import makedirs,listdir,remove,rename
#import hashPasswd #ln -s 软连接 from .. import hashPasswd ide可解析 但是报错
from sqlalchemy.orm import Session

from tmpprj.databases import home_db
from tmpprj.databases.session import get_db
from tmpprj.paths import FILES_DIR, STATIC_DIR
from tmpprj.security.token import tokenCk_Pattern
router = APIRouter()

from tmpprj.video import file_type



@router.get("/")
def home(request: Request,response: Response, session: Session = Depends(get_db),id: int = None,):
    res=tokenCk_Pattern(session, request,response)
    if(res==0):
        return (0,HTTPException(
                status_code=404,
                detail="没有token",))
    uid=res['id']
    print('uid is:'+str(uid))
    return '你是帅哥'

@router.get('/info')#token要判空!!!!
def info(request: Request,response: Response, session: Session = Depends(get_db)): 
    res=tokenCk_Pattern(session, request,response)
    if(res==0):
        return (0,HTTPException(
                status_code=404,
                detail="没有token",))                                    #这个判断没有作用   
    return {'usr_name':res['usr_name'],'id':res['id']}

@router.get('/finish_file/{file_name}')
async def file_all_in_one(request:Request,response: Response,file_name:str,
                            n:int=0,session: Session = Depends(get_db)):
    uinfo=tokenCk_Pattern(session, request,response)
    if(uinfo==0):
        return HTTPException(
                status_code=404,
                detail="没有token",)
    #=====================================#
    save_path = f"{FILES_DIR}/{uinfo['id']}/{file_name}/"
    try:
        with open(save_path+'-10__memo__','r') as memo: 
            data=memo.readline()+'}'
            rst=json.loads(data)
    except:
        rst={0,'no'}

    return rst


@router.post('/upload_f')
async def upload_file(
    request:Request,
    response:Response,
    session: Session = Depends(get_db),
    blob: UploadFile =File(...),
    hash:str=Form(...),
    start:int=Form(...),
    end:int=Form(...),
    index:str=Form(...),
    file_name:str=Form(...)
):  
    #print('文件名'+file_name)
    uinfo=tokenCk_Pattern(session, request,response)
    if(uinfo==0):
        return HTTPException(
                status_code=404,
                detail="没有token",)
    #创建路经
    save_path = f"{FILES_DIR}/{uinfo['id']}/{file_name}/"
    file_save_name=save_path+index+'__'+hash

    print(file_save_name)
    #print("HASH:"+hash)
    file_data=await blob.read()
    file_md5=hashlib_md5(file_data).hexdigest()
    #print("校验md5:"+file_md5)
    if(file_md5!=hash):
        print("校验失败")
        return HTTPException(
                status_code=404,
                detail="校验失败",)

    if not exists(save_path):
        makedirs(save_path)
    #存文件
    with open(file_save_name, "wb+") as buffer:
        buffer.write(file_data)
    #记录完成的文件
    with open(save_path+'-10__memo__','a+') as Memo:
        if(Memo.tell()==0):
            Memo.write(('{"'+index+'"'+':'+'"'+hash+'"'))
        else:
            Memo.write((',"'+index+'"'+':'+'"'+hash+'"'))
   

    return HTTPException(
            status_code=114514,
            detail="校验成功",)

@router.get('/upload_f_end/{file_name}')
async def file_all_in_one(request:Request,response: Response,file_name:str,n:str='None',cc:int=0,session: Session = Depends(get_db)):    
    uinfo=tokenCk_Pattern(session, request,response)
    if(uinfo==0):
        return HTTPException(
                status_code=404,
                detail="没有token",)

    save_path = f"{FILES_DIR}/{uinfo['id']}/{file_name}/"
    chunks = listdir(save_path)
    if(len(chunks)-1<cc):
        return HTTPException(
            status_code=401,
            detail="文件不完整,可能由于重复上传",)
    chunks.sort(key=lambda x:int(x.split('__')[0]))

    done_path = f"{FILES_DIR}/{uinfo['id']}/__done/{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}{n}__{file_name}/"

    """ t=datebases.home_db.save_video(done_path,uinfo['id'],n,'info_tmp')
    if(t==0):
        with open(f"{FILES_DIR}/{uinfo['id']}/__fail", 'a+') as Memo:
            Memo.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+save_path+'\n')
        return HTTPException(
                status_code=404,
                detail="存档失败",) """
    
    if not exists(done_path):
        makedirs(done_path)
    with open(done_path+n, "wb+") as merge:
        for chunk in chunks[1:]:
            with open(save_path+chunk,'rb') as buffer:
                merge.write(buffer.read())
            remove(save_path+chunk)

    f_type=file_type(done_path+n)
    if(f_type in ['text/html',]):
        rename(done_path+n, done_path+n+'.txt')
        print('jbb'+f_type)
        n+='.txt'
        
    t=home_db.save_video(session, done_path,uinfo['id'],n,file_type(done_path+n),'info_tmp')
    if(t==0):
        with open(f"{FILES_DIR}/{uinfo['id']}/__fail", 'a+') as Memo:
            Memo.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+save_path+'\n')
        return HTTPException(
                status_code=404,
                detail="存档失败",)
    
    return HTTPException(
            status_code=200,
            detail="上传成功",)

    
@router.get('/my_file')
async def my_file(request:Request,response:Response,session: Session = Depends(get_db)):
    uinfo=tokenCk_Pattern(session, request,response)
    if(uinfo==0):
        return HTTPException(
                status_code=404,
                detail="没有token",)
    uid=uinfo['id']
    return home_db.my_video(session, uid)
