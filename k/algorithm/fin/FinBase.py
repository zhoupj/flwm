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

            print("run error. code:", code);
            print(e.__traceback__)
            msg = traceback.format_exc()  # 方式1
            print(msg)
            __err_df=pd.DataFrame();
            __err_df.loc[0, 'class'] = self.__class__.__name__;
            __err_df.loc[0, 'code'] = code;
            __err_df.loc[0, 'date'] = datetime.date.today();
            __err_df.loc[0, 'err'] = e.__traceback__.__class__
            __err_df.to_csv('../../log/algorithm-fin-error.log',mode='a');

            return False;

    def __query(self,code,type):
        pm = PandasToMysql.instance();
        df=pm.query(DbCreator.share_data_finance,where=' code=\''+code+'\' and fin_type=\''+str(type)+'\' order by fin_date desc');
        pm.close();
        return df;

    def _process(self,df):
        return;




