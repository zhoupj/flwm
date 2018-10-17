import traceback;
import datetime;
import pandas as pd;
from k.util.Logger import Logger;
from k.util.PandasToMysql import PandasToMysql;

class TBasePuller:

    def pull(self,dt=None,to_mysql=True,to_csv=False):
        try:
          Logger.log('pull tbase data,dt',dt)
          df=  self._run(dt);
          if (to_mysql):
                pm = PandasToMysql();
                self._save_to_mysql(pm,df);
          if (to_csv):
                self._save_to_csv(df)
          return df;
        except Exception as e:
            print('pull tbase  error. dt:',dt);
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

    def _run(self,dt=None):
        return;


    def query_from_mysql(self,code=None):
        return;