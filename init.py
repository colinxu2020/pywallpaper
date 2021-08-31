"""
Init script for Pywallpaper.

Used Application:
    PyWallpaper(https://github.com/colinxu2020/pywallpaper)
Author:
    Colinxu2020
Version:2021.8.30
Last Update: 2021.8.30 21:39(UTC+8)
FilePath: /libs.py
Version Change:
    2021.8.30: Add this docs string.
    ...
Functions:
    None
"""

from sys import argv
from pip._internal.cli.main import main as pip
from libs import setencoding

setencoding()
with open('requirements.txt') as f:
    packages=f.read().split('\n')
if '--no-gui' in argv:
    del packages[packages.index('Pillow')]
if '--no-sched' in argv:
    del packages[packages.index('schedule')]
pip(['install']+packages)