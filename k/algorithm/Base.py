import traceback;
import datetime;
import pandas as pd;
from k.util.Logger import  Logger;
from k.Config import Config;
import  numpy as np;
from k.util.PandasToMysql import PandasToMysql;
from k.util.DbCreator import  DbCreator;

class Base:

    _default_value=None;

    def run(self,code,df,start=0,to_mysql=False,to_csv=False):

        try:
            Logger.log('start to run,code:',code,',factor:',self.__class__.__name__);

            if (df.empty or df.shape[0] == 0):
                Logger.log('empty df to run,factor:', self.__class__.__name__);
                return;

            df=self._process(df,start);

            if(to_mysql):
                df=df.loc[start:,:];
                pm=PandasToMysql();
                pm.update(DbCreator.share_data_day,df,primaryKeys=[Config.id])
                pm.close();

            if(to_csv):
                df.to_csv('../data/algrithm/'+code+'.csv');

            Logger.log('end to run,code:', code, ',factor:', self.__class__.__name__);
            return True;

        except Exception  as e:
            Logger.exception(self.__class__.__name__,code,str(start))
            return False;

    # def __query(self,code):
    #     pm=PandasToMysql.instance();
    #     df = pm.query(DbCreator.share_data_day, where='code=\'' + code + '\' and trade_date>=\'2016-01-01\'');

    def _process(self,df,start):
        return;




