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
            Logger.exception(self.__class__.__name__, code, str(start))

    def _run(self,code,start,end):
        return;

    def _save_to_mysql(self,pm,df):
        return

    def _save_to_csv(self,code,df):
        return


    def query(self,code=None,start=None,end=None):
        return;