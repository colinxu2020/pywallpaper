
from libs import setWallPaper

__author__='colinxu2020'


if __name__=='__main__':
    day=input('请输入日期(0代表今天,1代表明天,-1代表昨天,以此类推)')
    setWallPaper(int(day))