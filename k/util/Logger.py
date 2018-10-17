import pandas as pd;
import  uuid;
import datetime;
import traceback;
import logging
import logging.handlers
import sys;

# 创建一个logger
digest_log=logging.getLogger('digest');
digest_log.setLevel(logging.INFO)
d_handler = logging.FileHandler('../log/digest.log')
d_handler.setLevel(logging.INFO)
d_handler.setFormatter(logging.Formatter("%(asctime)s|%(message)s"))
digest_log.addHandler(d_handler)


logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

rf_handler = logging.handlers.TimedRotatingFileHandler('../log/run.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
rf_handler.setFormatter(logging.Formatter("%(asctime)s|%(message)s"))

f_handler = logging.FileHandler('../log/error.log')
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter("%(asctime)s|%(message)s"))

logger.addHandler(rf_handler)
logger.addHandler(f_handler)


# logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
#                     filename='new.log',
#                     filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
#                     #a是追加模式，默认如果不写的话，就是追加模式
#                     format='%(asctime)s,%(message)s' #%(pathname)s,line:%(lineno)d,%(levelname)s,
#                     #日志格式
#                     )

class Logger:

   debug=True;

   @staticmethod
   def log(*args):
       if(Logger.debug):
           print(args)

       msg='';
       for a in args:
           msg=msg+str(a)+' ';
       logger.info(msg)


   @staticmethod
   def digest(type,code,dt,succ):
       digest_log.info(type+'|'+code+'|'+dt+'|'+str(succ))

   @staticmethod
   def exception(cls_name,code,dt):
       logger.error(cls_name+'|'+code+'|'+dt)
       logger.exception(sys.exc_info())
       #exp = traceback.format_exc()  # 方式1

   @staticmethod
   def exception():
       logger.exception(sys.exc_info())

   @staticmethod
   def error(info):
       logger.error(info)


if(__name__=='__main__'):
    # 记录一条日志
    Logger.digest('a','d','299999',True)
    try:
        raise Exception;
    except Exception as e:
        Logger.exception()
    Logger.log('a',122,'b','dddd')