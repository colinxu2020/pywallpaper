import urllib.request as req
from json import load
from os.path import abspath
from typing import IO, NoReturn

global filepath
__author__='colinxu2020'

def setencoding() -> NoReturn:
    """设置输出编码"""
    import io
    import sys
    sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
    sys.stdin=io.TextIOWrapper(sys.stdin.buffer,encoding='utf8')
    sys.stderr=io.TextIOWrapper(sys.stderr.buffer,encoding='utf8')

def getWallPapers(day:int=1) -> tuple:
    """获取壁纸"""
    from json import load
    if day<0:day=abs(day)
    else: day=-day 
    url=f'https://www.bing.com/HPImageArchive.aspx?format=js&idx={day}&n=1'
    headers={"User-Agent":""}
    ret=req.urlopen(req.Request(url,headers=headers))
    ret=load(ret)['images'][0]
    return ret['copyright'],'https://www.bing.com'+ret['url']

def readConfig(Key:str):
    from toml import load
    with open('config.toml') as f:
        config=load(f)[Key]
    return config

def writeWallPaper(link:str,name:str='wallpaper.jpg') -> str:
    from os.path import abspath
    filepath=abspath(readConfig('wallPaperCachePath'))+'/'+name
    with open(filepath,'wb') as f:
        ret = req.urlopen(link)
        f.write(ret.read())
    return filepath

def setWallPaper(index:int) -> NoReturn:
    import ctypes
    wallpaper=getWallPapers(index)
    _=ctypes.windll.user32.SystemParametersInfoW(20,0,writeWallPaper(wallpaper[1]),0)
