import urllib.request as req
from json import load
from os.path import abspath
from typing import IO, NoReturn
import toml
import io
import sys

global filepath
__author__='colinxu2020'

def readConfig(Key:str):
    """
    Argments:
        Key: 接受字符串,要读取的配置信息
    Return:
        不固定类型,为实际配置信息
    
    从config.toml读取指定的配置信息
    """
    with open('config.toml') as f:
        config=toml.load(f)[Key]
    return config

def setencoding() -> NoReturn:
    """
    Argment:
        None
    Return:
        None
    设置输出编码为UTF8
    """
    sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
    sys.stdin=io.TextIOWrapper(sys.stdin.buffer,encoding='utf8')
    sys.stderr=io.TextIOWrapper(sys.stderr.buffer,encoding='utf8')

def getSource():
    """
    Argment:
        None
    Return:
        None
    
    获取默认源
    """
    AutoSource=readConfig('autoSource')
    return readConfig('source')[AutoSource]

def getWallPapers(day:int=0) -> tuple:
    """
    Argments:
        day: 接受Int类型的数据,默认为0,0代表今天,1代表明天,-1代表昨天,以此类推
    Return:
        返回一个元组,包含图片名和链接
    
    获取壁纸
    """
    source=getSource()

    if day<0:day=abs(day)
    else: day=-day 
    url=source['url'].format(day=day)
    headers={"User-Agent":""}
    ret=req.urlopen(req.Request(url,headers=headers))

    locals_={'ret':ret}
    exec(source['filter'],None,locals_)
    pic_title,link=locals_['pic_title'],locals_['links']

    return pic_title,link

def writeFileLikeObjectToFile(Object,filepath,byte=True) -> NoReturn:
    """
    Argment:
        Object:FileLikeObject
        filepath:要写入到的文件路径
    Return:
        None
    
    将一个FileLikeObject写入到文件
    """
    if byte: mode='wb'
    else: mode='w'
    with open(filepath,mode=mode) as f:
        f.write(Object.read())

def setWallPaper(index:int=0) -> NoReturn:
    """
    Argments:
        index: 接受整形,图片日期,以当日为0
    Return:
        None
    
    设置壁纸
    """
    import ctypes
    wallpaper=getWallPapers(index)
    filepath=abspath(f'{readConfig("wallPaperCachePath")}/wallpaper.jpg')
    writeFileLikeObjectToFile(req.urlopen(wallpaper[1]),filepath)
    _=ctypes.windll.user32.SystemParametersInfoW(20,0,filepath)
