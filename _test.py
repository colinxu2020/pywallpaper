import pytest
from libs import *

def test_getWallPaper():
    wallpaper=getWallPapers()
    assert wallpaper
    assert wallpaper[0]
    assert wallpaper[1]

def _test_testWallPaperFileWrite():
    byte=None
    writeWallPaper('https://bing.ioliu.cn/photo/BarnettsDemesne_ZH-CN8484261440?force=download','test.jpg')
    with open(filepath.replace('wallpaper.jpg','temp.jpg')) as f:
        assert f.read()==None