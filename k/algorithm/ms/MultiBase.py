from k.Config import Config;
from k.util.DbCreator import DbCreator;
from k.util.Logger import logger, digest_log;
from k.util.PandasToMysql import pm;


# 计算多个code 之间的关系
class MultiBase:

    _default_value = None;

    def run(self, df,dt,to_mysql=False):
        succ=True;
        try:

            if (df.empty or df.shape[0] == 0):
                logger.info('no data to run for mlt base')
            else:
                df= self._process(df);
                if(to_mysql):
                    pm.update(DbCreator.share_data_day,df,primaryKeys=[Config.id])
        except Exception  as e:
           succ=False;
           logger.exception('muliti base error')

        digest_log.info('Alg-mlt|%s|%s|%s'%(self.__class__.__name__,dt,succ))

    def _process(self, df):
        return;