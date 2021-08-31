"""
Better log support.

Used Application:
    SVG Generator
    PyWallpaper(https://github.com/colinxu2020/pywallpaper)
Author:
    Colinxu2020
Version:2021.8.30
Last Update: 2021.8.31 10:22(UTC+8)
FilePath: /logger.py
Version Change:
    2021.8.30: Add this docs string, support for if log3py not found
    2021.8.24: Create this file.
"""

from sys import argv

try:
    from log3py import Logger
except ModuleNotFoundError:
    from logging import Logger

__version__ = '20210824'
__author__ = ['Colinxu2020']

argv = argv[1:]
kv = {}
for idx, arg in enumerate(list(argv)):
    if arg.startswith('--logging.'):
        del argv[idx]
        arg = arg[10:].split('=')
        kv[arg[0]] = arg[1]
logger = Logger(**kv)
