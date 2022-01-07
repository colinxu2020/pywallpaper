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

def get_page(url, headers: dict[str, str]=None):
    """
    Get a page from network.
    
    Arguments:
        url: Remote address.
    """
    if headers is None:
        headers = {}
    headers.setdefault("user-agent", "Python/Urllib/Pywallpaper/Spider keyword:Gecko")
    return req.urlopen(req.Request(url, headers=headers))  # skipcq: BAN-B310  # This is INTENTIONAL, this is use to allow user define special url. 


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
    pkg_locals = {"ret": ret}
    try:
        for pkg in source["need_packages"]:
            locals[pkg] = __import__(pkg)
    except KeyError:
        pass

    exec(source["filter"], None, pkg_locals)  # skipcq: PYL-W0122  # This is INTENTIONAL to run USER DEFINED filter script.
    pic_title, link = pkg_locals["pic_title"], pkg_locals["links"]

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
        if not (hasattr(fp, "writable") and fp.writable()):
            raise TypeError("File object most be writable")
        if not content:
            raise ValueError("Text in file like object most not be empty")
        fp.write(content)


def set_wallpaper(index: int = 0) -> None:
    """
    Set wallpaper from source in config.

    Arguments:
        index: Photo index, 0 for today.
    """
    import ctypes

    wallpaper = get_wallpaper(index)
    filepath = abspath(f'{read_config("wallPaperCachePath")}/wallpaper.jpg')
    write_file_like_object_text_to_file(get_page(wallpaper[1]), filepath, "wb")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath)
