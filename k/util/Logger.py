import datetime;
import logging.handlers

from GlobalConfig import ConfigDict;


class MyLogUtil:

   def __init__(self,PATH,debug,console):
        # 创建一个logger
        digest_log=logging.getLogger('digest');
        digest_log.setLevel(logging.INFO)
        d_handler =logging.handlers.TimedRotatingFileHandler(PATH+'digest.log', when='midnight', interval=1, backupCount=7,
                                                  atTime=datetime.time(0, 0, 0, 0))
        d_handler.setLevel(logging.INFO)
        d_handler.setFormatter(logging.Formatter("%(asctime)s|%(message)s"))

        logger = logging.getLogger('mylogger')
        if(debug=='true'):
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        rf_handler = logging.handlers.TimedRotatingFileHandler(PATH+'run.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
        rf_handler.setFormatter(logging.Formatter("%(asctime)s|%(message)s"))

        f_handler = logging.FileHandler(PATH+'error.log')
        f_handler.setLevel(logging.ERROR)
        f_handler.setFormatter(logging.Formatter("%(asctime)s|%(pathname)s|%(lineno)d|%(message)s"))

        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(logging.Formatter("%(asctime)s|%(message)s")) #设置屏幕上显示的格式

        logger.addHandler(rf_handler)
        logger.addHandler(f_handler)

        digest_log.addHandler(d_handler)
        digest_log.addHandler(rf_handler)

        if(console=='true'):
            logger.addHandler(sh)
            digest_log.addHandler(sh)

        self.logger=logger;
        self.digest_log=digest_log;


ml=MyLogUtil(ConfigDict['k_log_path'],ConfigDict['debug'],ConfigDict['console'])
logger=ml.logger;
digest_log=ml.digest_log;

# logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
#                     filename='new.log',
#                     filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
#                     #a是追加模式，默认如果不写的话，就是追加模式
#                     format='%(asctime)s,%(message)s' #%(pathname)s,line:%(lineno)d,%(levelname)s,
#                     #日志格式
#                     )


if(__name__=='__main__'):
    # 记录一条日志
    logger.info("test la lala")
    try:
        raise Exception;
    except Exception as e:
        logger.exception("error")