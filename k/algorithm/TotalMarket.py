from k.algorithm.Base import Base;
from k.Config import Config;
import  numpy as np;
import pandas as pd;
from k.util.PandasToMysql import pm;
from k.util.DbCreator import DbCreator;

class TotalMarket(Base):

    def _process(self,df,start):
        code=df.loc[0,Config.code];
        basic_df=pm.query(DbCreator.share_base,where=' code="%s"'%(code));
        print(basic_df.loc[0,Config.totals])
        df[Config.totals]=df[Config.close]*basic_df.loc[0,Config.totals];

        return df[[Config.id,Config.totals]];


#main
if (__name__ == '__main__'):
    df = pm.query(DbCreator.share_data_day, where='code=\'000860\' and trade_date>=\'2018-10-10\'');
    print(df[[Config.id,Config.db_date,Config.totals,Config.close]]);
    tm=TotalMarket();
    tm.run('000860',df)
    print(df[[Config.id,Config.totals,Config.close]])
