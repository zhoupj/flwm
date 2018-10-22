import schedule
import time
import datetime;
from k.manager.FinManager import FinManager;
from k.puller.SharePuller import SharePuller;
from k.manager.Kmanager import KManager;
from k.util.Logger import logger;

def job_month():

    sp = SharePuller();
    sp.pull();

    FinManager.pull_data();
    FinManager.count_kpi();

def job_day():

    td=datetime.datetime.now().strftime('%Y-%m-%d');
    logger.info('schedule job start to work:'+td);
    KManager.pull_data(td);
    KManager.count_kpi(td);

def job_min():
    td = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
    print('schedule:'+td)

schedule.every(30).days.at("23:00").do(job_month)
schedule.every().days.at("18:30").do(job_day)
schedule.every().days.at("23:30").do(job_day)
schedule.every(5).seconds.do(job_min)


while True:
    schedule.run_pending()
    time.sleep(5)
