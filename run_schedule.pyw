import time
import schedule
import libs

schedule.every().day.at(libs.readConfig('schedule')['updateTime']).do(libs.setWallPaper)

def run():
    while 1:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run()