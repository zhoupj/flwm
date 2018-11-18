from k.algorithm.Base import Base;
from k.util.DbCreator import  DbCreator;
from k.Config import Config;
from k.util.FactorUtil import FactorUtil;
import  numpy as np;
import pandas as pd;

MONTH_COUNT=11;#从0开始

class MonthReverse(Base):

    def _process(self,df,start):

        for i in range(start, df.shape[0], 1):

            df.loc[i, 'ha']=0;
            df.loc[i, 'hb'] = 0;
            df.loc[i, 'la'] = 0;
            df.loc[i, 'lb'] = 0;
            df.loc[i, 'h_reverse'] = 0;
            df.loc[i, 'l_reverse'] = 0;

            if(i>=11):
                a,b=FactorUtil.best_coordinate_for_trend(df.loc[i-11:i,'high'].values);
                df.loc[i,'ha']=a;
                df.loc[i,'hb']=b;
                a, b = FactorUtil.best_coordinate_for_trend(df.loc[i - 11:i, 'low'].values,direct='l');
                df.loc[i, 'la'] = a;
                df.loc[i, 'lb'] = b;
            if(i>=12):
                df.loc[i,'h_reverse']=FactorUtil.is_reverse(df.loc[i-1,'ha'],df.loc[i-1,'hb'],df.loc[i,'close']);
                df.loc[i, 'l_reverse'] = FactorUtil.is_reverse(df.loc[i - 1, 'la'], df.loc[i - 1, 'lb'],
                                                               df.loc[i, 'close'],direct='l');

        return df[[Config.id, 'ha','hb','la','lb','h_reverse','l_reverse']];


    def _get_update_table_name(self):
        return DbCreator.share_data_month;


#main
if (__name__ == '__main__'):
    mr=MonthReverse();
    df=mr.query_test_data('300394',tb_name=DbCreator.share_data_month)
    print(df);
    mr.run('300394',df,start=0,to_mysql=True);

