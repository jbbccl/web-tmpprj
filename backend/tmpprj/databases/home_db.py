# 只在“直接运行本文件”时把包根目录加进搜索路径。
# 用 __file__ 定位，不依赖当前工作目录；被 import 时这段不执行。
if __name__ == "__main__":
    import pathlib
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import time

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Session

from tmpprj.databases.db_info import Base, engine


class usrs_info(Base):
    __tablename__ = "usrs_info"
    id = Column(Integer, primary_key=True, unique=True)  # index=True
    path = Column(String(128), unique=True)
    name = Column(String(32))
    data = Column(DateTime, default=None)
    bak = Column(String(256), default=None)
    bak1 = Column(String(256), default=None)


class videos(Base):
    __tablename__ = "videos"
    vid = Column(Integer, primary_key=True, unique=True)  # index=True
    path = Column(String(256))
    v_name = Column(String(256), default=None)
    info = Column(String(256), default=None)
    uper_id = Column(Integer)
    date = Column(DateTime, default=None)
    type = Column(String(128), default=None)
    like = Column(Integer, default=0)


# ↓ 同 db.py：session 由 FastAPI 注入，不再自己 SessionLocal()
def save_video(session: Session, PATH, UID, V_NAME, filetype, INFO=None):
    try:
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        aVideo = videos(path=PATH, v_name=V_NAME, info=INFO,
                        uper_id=UID, date=now_time, type=filetype)
        session.add(aVideo)
        session.commit()
        return 1
    except Exception:
        session.rollback()
        return 0


def get_video(session: Session, vid):
    video = session.query(videos).filter(videos.vid == vid).first()
    if video is None:
        return 0
    print(video.path)
    print(video.uper_id)
    return {'path': video.path,
            'v_name': video.v_name,
            'date': video.date,
            'type': video.type,
            'info': video.info,
            'uper_id': video.uper_id,
            'like': video.like}


def get_video_list(session: Session, index: int, count: int):
    rst = []
    video = session.query(videos).order_by(videos.vid.desc()).slice(index, index + count)
    for i in video:
        rst.append({
            'vid': i.vid,
            'v_name': i.v_name,
            'date': i.date,
            'type': i.type,
            'info': i.info,
            'uper_id': i.uper_id,
            'like': i.like})
    return rst


def my_video(session: Session, uid):
    rst = []
    my_vid_list = session.query(videos).filter(videos.uper_id == uid)
    for i in my_vid_list:
        rst.append({
            'vid': i.vid,
            'v_name': i.v_name,
            'date': i.date,
            'type': i.type,
            'info': i.info,
            'uper_id': i.uper_id,
            'like': i.like})
    return rst
