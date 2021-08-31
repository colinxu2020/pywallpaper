"""
Entrypoint of Pywallpaper

Used Application:
    PyWallpaper(https://github.com/colinxu2020/pywallpaper)
Author:
    Colinxu2020
Version:2021.8.30
Last Update: 2021.8.30 21:37(UTC+8)
FilePath: /config.py
Version Change:
    2021.8.30: Add this docs string.
Function:
    None
    ...
"""

from libs import set_wallpaper


if __name__ == '__main__':
    day = input('请输入日期(0代表今天,1代表明天,-1代表昨天,以此类推)')
    set_wallpaper(int(day))
