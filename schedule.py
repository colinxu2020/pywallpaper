import threading
import time
import schedule
import libs

schedule.every().day.at(libs.readConfig('time')).do(libs.setWallPaper)

def run():
    while 1:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run).start()