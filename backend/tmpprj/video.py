import os
from fastapi import APIRouter,HTTPException,Response,Request,UploadFile,File,Form,Depends
from fastapi.responses import FileResponse,StreamingResponse

from pydantic import BaseModel
from  mimetypes import guess_type
from hashlib import md5 as hashlib_md5
from os import makedirs,listdir,remove
from sqlalchemy.orm import Session

# 注意：这个 router 故意**不**挂鉴权依赖。
# 前端是用 <video src="/api/home/video/3"> 直接播的，浏览器为 <video> 发不出自定义请求头，
# 一旦要求 token 头，播放会直接失败（这正是原来那段判断被注释掉的原因）。
# 要给视频加鉴权，得先把 token 换成 cookie 或签名 URL。
from tmpprj.databases import home_db
from tmpprj.databases.session import get_db

router = APIRouter()


def is_video(file_path):
    image_mimetypes = ['image/jpeg', 'image/png', 'image/gif']
    file_mime_type = guess_type(file_path)[0]
    print('文件类型: '+(file_mime_type))
    return file_mime_type in image_mimetypes
def file_type(file_path):
    file_mime_type = guess_type(file_path)[0]
    return str(file_mime_type)

@router.get('/{vid}')
async def file_all_in_one(request:Request,response: Response,vid:int,session: Session = Depends(get_db)):
    # 这里故意不做鉴权，原因见文件开头。
    res=home_db.get_video(session, vid)
    if res==0:
        return HTTPException(
                status_code=404,
                detail="无此视频",)
    return FileResponse(res['path']+res['v_name'],media_type=res['type'])

@router.get("/get/{vid}")
async def get_video_stream(request: Request,vid:int,session: Session = Depends(get_db)):
    res=home_db.get_video(session, vid)
    if res==0:
        return HTTPException(
                status_code=404,
                detail="无此视频",)
    request_range = request.headers.get("Range")
    try:
        range = int(request_range[request_range.find("=")+1: request_range.find("-")])
    except:
        range=0
    video_path = res['path']
    video_name = res['v_name']
    file_name = f"{video_path}/{video_name}"
    file_size = os.path.getsize(file_name)
    file_like = open(file_name, mode="rb")
    headers = {
        "Accept-Ranges": "bytes",
        "Content-Length": f"{file_size}",
        "Content-Type": "video/mp4",
        "Content-Disposition": f"attachment;file_name={video_name}",
        "Content-Range": f"{range + file_size - 1}"
    }
    return StreamingResponse(file_like, headers=headers)

@router.get('/get_list/{index}')
def vid_list(index:int,l:int=3,session: Session = Depends(get_db)):
    res=home_db.get_video_list(session, index, l)
    if(len(res)):
        return res
    return 0