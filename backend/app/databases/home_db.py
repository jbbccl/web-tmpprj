'''========添加引用路径========'''
from sys import path
from os.path import abspath 
path.append(abspath('.'))
'''============================'''
from databases.db_info import *
import time



class usrs_info(Base):
    __tablename__ = "usrs_info"
    id = Column(Integer, primary_key=True,unique=True)#index=True
    path = Column(String(128),unique=True)
    name = Column(String(32))
    data = Column(DateTime,default=None)
    bak= Column(String(256),default=None)
    bak1 = Column(String(256),default=None)

class videos(Base):
    __tablename__ = "videos"
    vid = Column(Integer, primary_key=True,unique=True)#index=True
    path = Column(String(256))
    v_name= Column(String(256),default=None)
    info = Column(String(256),default=None)
    uper_id = Column(Integer)
    date = Column(DateTime,default=None)
    type = Column(String(128),default=None)
    like=Column(Integer,default=0)

    
Base.metadata.create_all(bind=engine) #=============建表==============


def save_video(PATH,UID,V_NAME,filetype,INFO=None):
    with SessionLocal() as tmpsession:
        try:
            now_time= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            aVideo=videos(path=PATH,v_name=V_NAME,info=INFO,
                          uper_id=UID,date=now_time,type=filetype)
            tmpsession.add(aVideo)
            tmpsession.commit()

            return 1
        except:
            return 0
        
def get_video(vid):
    with SessionLocal() as usrSession:
        try:
            video = usrSession.query(videos).filter(videos.vid==vid).first()
        except:
            return 0
        print(video.path)
        print(video.uper_id)
        return {'path':video.path,
                'v_name':video.v_name,
                'date':video.date,
                'type':video.type,
                'info':video.info,
                'uper_id':video.uper_id,
                'like':video.like}

def get_video_list(index:int,len:int):
    with SessionLocal() as tmpsession:
        try:
            rst=[]
            video = tmpsession.query(videos).order_by(videos.vid.desc()).slice(index,index+len)
            for i in video:
                rst.append({
                'vid':i.vid,
                'v_name':i.v_name,
                'date':i.date,
                'type':i.type,
                'info':i.info,
                'uper_id':i.uper_id,
                'like':i.like})
            return rst
        except:
            return 0

def my_video(uid):
    with SessionLocal() as tmpsession:
        try:
            rst=[]
            my_vid_list = tmpsession.query(videos).filter(videos.uper_id==uid)
            for i in my_vid_list:
                    rst.append({
                    'vid':i.vid,
                    'v_name':i.v_name,
                    'date':i.date,
                    'type':i.type,
                    'info':i.info,
                    'uper_id':i.uper_id,
                    'like':i.like})
            return rst
        except:
            return 0
#save_video('d00a6b458f649c44b',2,'1')
#get_video(1)
#res=get_video_list(1,3)
#print(res) 