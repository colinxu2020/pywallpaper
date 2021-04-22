"""
PyWallpaper main entry point.

Author: colinxu2020
"""

from libs import set_wallpaper


if __name__ == '__main__':
    day = input('请输入日期(0代表今天,1代表明天,-1代表昨天,以此类推)')
    set_wallpaper(int(day))
