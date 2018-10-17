import traceback;
import datetime;
import pandas as pd;
from k.util.Logger import Logger;
from k.util.PandasToMysql import PandasToMysql;

class FinBasePuller:

    def pull(self,year:int,season:int,to_mysql=True,to_csv=False):
        try:
          Logger.log('pull fin data,year',year,'season',season)
          df= self._run(year,season);
          if (to_mysql):
                pm = PandasToMysql();
                self._save_to_mysql(pm,df);
          if (to_csv):
                self._save_to_csv(df)
          return df;
        except Exception as e:
            Logger.exception(self.__class__.__name__, '', str(year)+str(season))
            return None;

    def _save_to_mysql(self, pm,df):
        return

    def _save_to_csv(self,df):
        return

    def _run(self,year,season):
        return;


    def query_from_mysql(self,code=None):
        return;