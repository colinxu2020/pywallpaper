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