import schedule
import time
import datetime;
from k.manager.FinManager import FinManager;
from k.puller.SharePuller import SharePuller;
from k.manager.Kmanager import KManager;
from k.util.Logger import logger;
from k.util.DateUtil import DateUtil;
import calendar;


def isWeekDay():
    # cal =calendar.week
    # if (cal.get(calendar.DAY_OF_WEEK) == calendar.SATURDAY or cal.get(calendar.DAY_OF_WEEK) == calendar.SUNDAY):
    #     return True;
    return False;

def job_every_month():

    if(isWeekDay()):
       return

    sp = SharePuller();
    sp.pull();

    FinManager.pull_data();
    FinManager.count_kpi();

def job_every_day():

    if (isWeekDay()):
        return

    td=datetime.datetime.now().strftime('%Y-%m-%d');
    logger.info('schedule job start to work:'+td);
    KManager.pull_data(td);
    KManager.pull_data_hk(td);
    KManager.pull_data_hk(DateUtil.getLastDay(td))
    KManager.count_kpi(td);

def job_min():

    print(isWeekDay())
    td = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
    print('schedule:'+td)


schedule.every(15).days.at("23:00").do(job_every_month)
schedule.every().days.at("18:30").do(job_every_day)
schedule.every().days.at("23:30").do(job_every_day)
#schedule.every(5).seconds.do(job_min)


while True:
    schedule.run_pending()
    print('schedule run')
    time.sleep(5)
