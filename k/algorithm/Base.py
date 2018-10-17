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
            df=self._process(df,start);

            if(to_mysql):
                pm=PandasToMysql();
                pm.update(DbCreator.share_data_day,df,primaryKeys=[Config.id])
                pm.close();

            if(to_csv):
                df.to_csv('../data/algrithm/'+code+'.csv');

            Logger.log('end to run,code:', code, ',factor:', self.__class__.__name__);

            return True;

        except Exception  as e:

            print("run error. code:", code);
            print(e.__traceback__)
            msg = traceback.format_exc()  # 方式1
            print(msg)
            __err_df=pd.DataFrame();
            __err_df.loc[0, 'class'] = self.__class__.__name__;
            __err_df.loc[0, 'code'] = code;
            __err_df.loc[0, 'date'] = datetime.date.today();
            __err_df.loc[0, 'err'] = e.__traceback__.__class__
            __err_df.to_csv('../log/algorithm-error.log',mode='a');

            return False;

    # def __query(self,code):
    #     pm=PandasToMysql.instance();
    #     df = pm.query(DbCreator.share_data_day, where='code=\'' + code + '\' and trade_date>=\'2016-01-01\'');

    def _process(self,df,start):
        return;




