import urllib.request as req
from json import load
from os.path import abspath
import typing
import toml
import io
import sys


__author__ = 'colinxu2020'


def read_config(Key: str) -> typing.Any:
    """
    Argments:
        Key: 接受字符串,要读取的配置信息
    Return:
        不固定类型,为实际配置信息

    从config.toml读取指定的配置信息
    """
    with open('config.toml') as f:
        config = toml.load(f)[Key]
    return config


def get_source() -> dict[str, str]:
    """
    Argment:
        None
    Return:
        None

    获取默认源
    """
    AutoSource = read_config('autoSource')
    return read_config('source')[AutoSource]


def get_wallpaper(day: int = 0) -> tuple:
    """
    Argments:
        day: 接受Int类型的数据,默认为0,0代表今天,1代表明天,-1代表昨天,以此类推
    Return:
        返回一个元组,包含图片名和链接

    获取壁纸
    """
    source = get_source()
    day = -day
    url = source['url'].format(day=day)
    headers = {"User-Agent": ""}
    ret = req.urlopen(req.Request(url, headers=headers))

    locals = {'ret': ret}
    exec(source['filter'], None, locals)
    pic_title, link = locals['pic_title'], locals['links']

    return pic_title, link


def write_file_like_object_text_to_file(file_like_object, filepath: str, mode = 'w') -> None:
    """
    Argment:
        Object:FileLikeObject
        filepath:要写入到的文件路径
        byte:bool
    Return:
        None

    将一个FileLikeObject写入到文件
    """
    with open(filepath, mode) as fp:
        assert fp.writable(), 'file object most be writable' 
        fp.write(file_like_object.read())


def set_wallpaper(index: int = 0) -> None:
    """
    Argments:
        index: 接受整形,图片日期,以当日为0
    Return:
        None

    设置壁纸
    """
    import ctypes


    wallpaper = get_wallpaper(index)
    filepath = abspath(f'{read_config("wallPaperCachePath")}/wallpaper.jpg')
    write_file_like_object_text_to_file(req.urlopen(wallpaper[1]), filepath, 'wb')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath)
