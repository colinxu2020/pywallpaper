"""
The library of pywallpaper.

Author: colinxu2020

Functions:
    read_config: read config file
    get_source: get default source
    get_wallpaper: get wallpaper
    write_file_like_object_text_to_file: write file like object's text to file
    set_wallpaper: set wallpaper
"""

import urllib.request as req
from os.path import abspath
import typing
import toml


def read_config(Key: str) -> typing.Any:
    """
    Read config file.

    Arguments:
        Key: key name of the configuration information to be read
    """
    with open('config.toml') as f:
        config = toml.load(f)[Key]
    return config


def get_source() -> dict[str, str]:
    """Get default source."""
    AutoSource = read_config('autoSource')
    return read_config('source')[AutoSource]


def get_wallpaper(day: int = 0) -> tuple:
    """
    Get wallpaper from source in config(include image name and image url).

    Arguments:
        day： 0 for today, 1 for tomorrow, -1 for yesterday, and so on (default: 0)
    """  # noqa: E501
    source = get_source()
    day = -day
    url = source['url'].format(day=day)
    headers = {"User-Agent": ""}
    ret = req.urlopen(req.Request(url, headers=headers))

    locals = {'ret': ret}
    exec(source['filter'], None, locals)
    pic_title, link = locals['pic_title'], locals['links']

    return pic_title, link


def write_file_like_object_text_to_file(
        file_like_object, filepath: str,
        mode: typing.Optional[str] = None) -> None:
    """
    Write text of object has read attribute to file.

    Argument:
        file_like_object: file link object
        filepath: path of the file will write to.
        mode: the mode of open file will write to.
    """
    if mode is None:
        mode = 'w' + file_like_object.mode[1:]
    with open(filepath, mode) as fp:
        content = file_like_object.read()
        assert fp.writable(), 'file object most be writable'
        assert content, 'text in file_link_objct most not None'
        fp.write(content)


def set_wallpaper(index: int = 0) -> None:
    """
    Set wallpaper from source in config.

    Arguments:
        index: 接受整形,图片日期,以当日为0
    """
    import ctypes

    wallpaper = get_wallpaper(index)
    filepath = abspath(f'{read_config("wallPaperCachePath")}/wallpaper.jpg')
    write_file_like_object_text_to_file(
        req.urlopen(wallpaper[1]), filepath, 'wb')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath)
