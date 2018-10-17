import traceback;
import datetime;
import pandas as pd;
from k.util.Logger import  Logger;
from k.util.PandasToMysql import PandasToMysql;
from k.util.DbCreator import DbCreator;
from k.Config import  Config;

# 计算多个code 之间的关系
class MultiBase:

    _default_value = None;

    def run(self, df,to_mysql=False):
        try:
            Logger.log('start to run,factor:', self.__class__.__name__);
            if (df.empty or df.shape[0] == 0):
                Logger.log('empty df to run,factor:', self.__class__.__name__);
                return;
            df= self._process(df);
            if(to_mysql):
                pm=PandasToMysql();
                pm.update(DbCreator.share_data_day,df,primaryKeys=[Config.id])
                pm.close()
            Logger.log('end to run,factor:');
        except Exception  as e:
            dt=df.loc[0,Config.db_date];
            Logger.exception(self.__class__.__name__, '', str(dt))


    def _process(self, df):
        return;