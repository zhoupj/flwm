import traceback;
import datetime;
import pandas as pd;
from k.util.PandasToMysql import pm;
from k.util.Logger import  logger,digest_log;

class TBasePuller:

    def pull(self,dt=None,to_mysql=True,to_csv=False):
        succ=True;
        df=None;
        try:
          df=  self._run(dt);
          if(df.empty):
              logger.info('get empty df for '+self.__class__.__name__);
          else:
              if (to_mysql):
                    self._save_to_mysql(pm,df);
              if (to_csv):
                    self._save_to_csv(df)
        except Exception as e:
            logger.exception('tbase puller error')
            succ=False;
        digest_log.info('t-puller|%s|%s|%s|%s' % (self.__class__.__name__, dt,str(to_mysql),succ))
        return df;
    def _save_to_mysql(self, pm,df):
        return

    def _save_to_csv(self,df):
        return

    def _run(self,dt=None):
        return;


    def query_from_mysql(self,code=None):
        return;