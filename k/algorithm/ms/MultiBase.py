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
            df= self._process(df);
            if(to_mysql):
                pm=PandasToMysql();
                pm.update(DbCreator.share_data_day,df,primaryKeys=[Config.id])
                pm.close()
            Logger.log('end to run,factor:');
        except Exception  as e:
            print("run error. code:", self.__class__.__name__ );
            print(e.__traceback__)
            msg = traceback.format_exc()  # 方式1
            print(msg)
            __err_df=pd.DataFrame();
            __err_df.loc[0, 'class'] = self.__class__.__name__;
            __err_df.loc[0, 'date'] = datetime.date.today();
            __err_df.loc[0, 'err'] = e.__traceback__.__class__
            __err_df.to_csv('../log/algorithm-multi-error.log', mode='a');

    def _process(self, df):
        return;