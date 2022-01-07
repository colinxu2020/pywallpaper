"""
Library of Pywallpaper.

Used Application:
    PyWallpaper(https://github.com/colinxu2020/pywallpaper)
Author:
    Colinxu2020
Version:2021.8.30
Last Update: 2021.8.30 21:39(UTC+8)
FilePath: /libs.py
Version Change:
    2021.8.31: Update
    2021.8.30: Add this docs string.
    ...
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

import config

config.check_is_enable("pywallpaper")


def read_config(key: str) -> typing.Any:
    """
    Read config file.

    Arguments:
        Key: key name of the configuration information to be read
    """
    return config.get_config("pywallpaper")[key]

    if headers is None:
        headers = {}
    headers.setdefault("user-agent", "Python/Urllib/Pywallpaper/Spider keyword:Gecko")
    return req.urlopen(req.Request(url, headers=headers))


def get_source() -> dict[str, str]:
    """Get default source."""
    defaultSource = read_config("defaultSource")
    return read_config("source")[defaultSource]


def get_wallpaper(day: int = 0) -> tuple:
    """
    Get wallpaper from source in config(include image name and image url).

    Arguments:
        day： 0 for today, 1 for tomorrow, -1 for yesterday, and so on (default: 0)
    """  # noqa: E501
    source = get_source()
    day = -day
    url = source["url"].format(day=day)
    ret = get_page(url)
    locals = {"ret": ret}
    try:
        for pkg in source["need_packages"]:
            locals[pkg] = __import__(pkg)
    except KeyError:
        pass

    exec(source["filter"], None, locals)
    pic_title, link = locals["pic_title"], locals["links"]

    return pic_title, link


def write_file_like_object_text_to_file(
    file_like_object, filepath: str, mode: typing.Optional[str] = None
) -> None:
    """
    Write text of object has read attribute to file.

    Argument:
        file_like_object: file link object
        filepath: path of the file will write to.
        mode: the mode of open file will write to.
    """
    if mode is None:
        mode = "w" + file_like_object.mode[1:]
    with open(filepath, mode) as fp:
        content = file_like_object.read()
        assert fp.writable(), "file object most be writable"
        assert content, "text in file_link_objct most not None"
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
    write_file_like_object_text_to_file(get_page(wallpaper[1]), filepath, "wb")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath)
