import pymysql
import threading
import time
#import asyncio

lock=threading.Lock()
reglock=1

db = pymysql.connect(
        host = '43.128.57.171', # 连接主机, 默认127.0.0.1 
        user = 'dbtmp',      # 用户名
        passwd = 'Dst123!@#',# 密码
        port = 3306,        # 端口，默认为3306
        db = 'dbtmp',        # 数据库名称
        charset = 'utf8'    # 字符编码
    )
#cursor = db.cursor()

def conndb():
    cursor = db.cursor()
    return cursor

def test(cursor):
    cursor.execute("select version()") # 返回值是查询到的数据数量
    # 通过 fetchall方法获得数据
    data = cursor.fetchone()
    print("Database Version:%s" % data)


def distruct(cursor):
    cursor.close()  # 关闭游标
    db.close()    # 关闭连接

def cknamerep(cursor,name,f=0):#   1=可以注册   2=用户名已被占用 0=error
    if(reglock==0):
        print('sorry not time, come out')
        return 1#'sorry not time, come out'
    try:
        lock.acquire(blocking=True)
        print('--开查')
        cursor.execute("select name from usr where name=%s",(name))
        name= cursor.fetchall()
        print('--查完')
        lock.release()
        print('用户名查重:',end='')
        print(f,end='')
        print(name)
        if(len(name) == 0):
            return 1
        else:
            return 2
    except pymysql.Error as e:
        print('ERRORORORORO000011000OREOOROOROER')
        print(e.args[0])
        print(e.args[1])
        return 0

    try:
        lock.acquire(blocking=False)
        cursor.execute("select name from usr where name=%s",(name))
        name= cursor.fetchall()
        lock.release()
        if(len(name) == 0):
            return 1
        else:
            return 2
    except pymysql.Error as e:
        print('ERRORORORORO000011000OREOOROOROER')
        print(e.args[0])
        return 0
    
def registry(cursor,name,passwd):#返回1为成功0失败
    try:
        #get uid
        global reglock
        reglock=0
        print(reglock)#locked

        lock.acquire()
        cursor.execute("select id from usr where name='记录id工具人' and pass='aaaaaaaaaaaaaaaaaaaa'")
        lock.release()

        id = cursor.fetchall()
        
        id=id[0][0]+1

        lock.acquire()
        cursor.execute("update usr set id=(%s) where name='记录id工具人' and pass='aaaaaaaaaaaaaaaaaaaa'",(id))
        lock.release()
        print('id is ',end=' :')
        print(id)
        sql = "insert into `usr`(`id`,`name`,`pass`) values (%s,%s,%s)"

        lock.acquire()
        cursor.execute(sql,(id,name,passwd))
        lock.release()
        db.commit()
        print('success')
        reglock=1
        return 1
    except pymysql.Error as e:
        print('ERROROROROROROEWOOROREOOROOROER')
        print(e.args[0])
        db.rollback()
        reglock=1
        return 0

#print(registry('test1','123'))多个线程调用execute 冲突

    try:
        print(name)
        cursor.execute("select name from usr where name=%s",(name))
        name= cursor.fetchall()
        print(name)
        cursor.execute("select name from usr where name=%s",(name))
        name= cursor.fetchall()
        print(name)
        cursor.execute("select name from usr where name=%s",(name))
        name= cursor.fetchall()
        print(name)
        cursor.execute("select name from usr where name=%s",(name))
        name= cursor.fetchall()
        print(name)   
        cursor.execute("select name from usr where name=%s",(name))
        name= cursor.fetchall()
        print(name)
        cursor.execute("select name from usr where name=%s",(name))
        name= cursor.fetchall()
        print(name)
        cursor.execute("select name from usr where name=%s",(name))
        name= cursor.fetchall()
        print(name)    
        if(len(name) == 0):
            return 1
        else:
            return 2
    except:
        db.rollback()
        return 0
#cknamerep('test1')
#i=0
##while i<5:
    name='q4'
    registry(name,'1221')
    ckname = cknamerep(name,100)
    i+=1