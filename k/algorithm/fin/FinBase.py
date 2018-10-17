import traceback;
import datetime;
import pandas as pd;
from k.util.Logger import  Logger;
from k.Config import Config;
import  numpy as np;
from k.util.PandasToMysql import PandasToMysql;
from k.util.DbCreator import  DbCreator;

class FinBase:

    _default_value=None;
    #type:1 季度，0 年度，2 累积 （2暂时无数据）
    def run(self,code,to_mysql=False,to_csv=False,type=1):
        try:
            df =self.__query(code,type);
            Logger.log('start to run fin code:',code,',factor:',self.__class__.__name__);
            df=self._process(df);

            if(to_mysql):
                pm=PandasToMysql.instance();
                pm.update(DbCreator.share_data_day,df,primaryKeys=[Config.id])
                pm.close();

            if(to_csv):
                df.to_csv('../data/algrithm/fin/'+code+'.csv');

            Logger.log('end to run,code:', code, ',factor:', self.__class__.__name__);

            return True;

        except Exception  as e:
            Logger.exception(self.__class__.__name__, code, '')
            return False;

    def __query(self,code,type):
        pm = PandasToMysql.instance();
        df=pm.query(DbCreator.share_data_finance,where=' code=\''+code+'\' and fin_type=\''+str(type)+'\' order by fin_date desc');
        pm.close();
        return df;

    def _process(self,df):
        return;




