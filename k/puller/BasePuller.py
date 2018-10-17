import traceback;
import datetime;
import pandas as pd;
from k.util.Logger import Logger;
from k.util.PandasToMysql import PandasToMysql;
from k.Config import Config;

class BasePuller:

    def pull(self,code:str,start:str,end:str,to_mysql=True,to_csv=False):
        try:
           Logger.log('pull data,code:',code,',start:',start,',end:',end);
           df= self._run(code,start,end);

           if(to_mysql):
                print(df);
                pm=PandasToMysql();
                self._save_to_mysql(pm,df);
                pm.close();
           if(to_csv):
                self._save_to_csv(code,df)
           return df;

        except Exception as e:
            print("puller run error. code:", code, );
            print(e.__traceback__)
            msg = traceback.format_exc()  # 方式1
            print(msg)
            __err_df=pd.DataFrame();
            __err_df.loc[0, 'class'] = self.__class__.__name__;
            __err_df.loc[0, 'code'] = code;
            __err_df.loc[0, 'date'] = datetime.date.today();
            __err_df.loc[0, 'err'] = e.__traceback__.__class__
            __err_df.to_csv('../log/puller-error.log', mode='a');
            return None;

    def _run(self,code,start,end):
        return;

    def _save_to_mysql(self,pm,df):
        return

    def _save_to_csv(self,code,df):
        return


    def query(self,code=None,start=None,end=None):
        return;