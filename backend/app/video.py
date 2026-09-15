import os
from fastapi import FastAPI,HTTPException,Response,Request,UploadFile,File,Form
from fastapi.responses import FileResponse,StreamingResponse

from pydantic import BaseModel
from threading import Lock
from  mimetypes import guess_type
import databases.home_db
from hashlib import md5 as hashlib_md5
from os import makedirs,listdir,remove
from scret import tocken
lock=Lock()

video_app = FastAPI()
#home_app.mount("/toor", StaticFiles(directory="toor"), name="toor")


def is_video(file_path):
    image_mimetypes = ['image/jpeg', 'image/png', 'image/gif']
    file_mime_type = guess_type(file_path)[0]
    print('文件类型: '+(file_mime_type))
    return file_mime_type in image_mimetypes
def file_type(file_path):
    file_mime_type = guess_type(file_path)[0]
    return str(file_mime_type)

@video_app.get('/{vid}')
async def file_all_in_one(request:Request,response: Response,vid:int):
    res=tocken.tokenCk_Pattern(request,response)
    """ if(res==0):
        return (0,HTTPException(
                status_code=404,
                detail="没有token",))   """  
    res=databases.home_db.get_video(vid)
    if res==0:
        return HTTPException(
                status_code=404,
                detail="无此视频",)
    return FileResponse(res['path']+res['v_name'],media_type=res['type'])

@video_app.get("/get/{vid}")
async def main(request: Request,vid:int):
    res=databases.home_db.get_video(vid)
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

@video_app.get('/get_list/{index}')
def vid_list(index:int,l:int=3):
    res=databases.home_db.get_video_list(index,l)
    if(len(res)):
        return res
    return 0