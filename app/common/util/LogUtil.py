import pandas as pd;
import  uuid;
import datetime;
import traceback;
import logging
import logging.handlers
import sys;
from GlobalConfig import ConfigDict;
PATH_DIR=ConfigDict['app_log_path']

# digest个logger
digest_log=logging.getLogger('digest');
digest_log.setLevel(logging.INFO)
d_handler = logging.FileHandler(PATH_DIR+'digest.log')
d_handler.setLevel(logging.INFO)
d_handler.setFormatter(logging.Formatter("%(asctime)s|%(message)s"))
digest_log.addHandler(d_handler)


# sugget_log
suggest_log=logging.getLogger('suggest');
suggest_log.setLevel(logging.INFO)
d_handler = logging.FileHandler(PATH_DIR+'suggest.log')
d_handler.setLevel(logging.INFO)
d_handler.setFormatter(logging.Formatter("%(asctime)s|%(message)s"))
suggest_log.addHandler(d_handler)


# run && error log
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

rf_handler = logging.handlers.TimedRotatingFileHandler(PATH_DIR+'run.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
rf_handler.setFormatter(logging.Formatter("%(asctime)s|%(message)s"))

f_handler = logging.FileHandler(PATH_DIR+'error.log')
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter("%(asctime)s|%(message)s"))

logger.addHandler(rf_handler)
logger.addHandler(f_handler)



if(__name__=='__main__'):
    # 记录一条日志
    logger.info('abc')
    try:
        raise Exception;
    except Exception as e:
       logger.exception('error')