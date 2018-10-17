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
            print('pull fin  error. year:',year,'season',season);
            print(e.__traceback__)
            msg = traceback.format_exc()  # 方式1
            print(msg)
            __err_df = pd.DataFrame();
            __err_df.loc[0, 'class'] = __class__.__name__;
            __err_df.loc[0, 'dt'] = dt;
            __err_df.loc[0, 'date'] = datetime.date.today();
            __err_df.loc[0, 'err'] = e.__traceback__.__class__
            __err_df.to_csv('../log/puller-t-error.log', mode='a');
            return None;

    def _save_to_mysql(self, pm,df):
        return

    def _save_to_csv(self,df):
        return

    def _run(self,year,season):
        return;


    def query_from_mysql(self,code=None):
        return;