from k.algorithm.Base import Base;
from k.util.DateUtil import DateUtil;
from k.util.PandasToMysql import pm;
from k.util.DbCreator import  DbCreator;
from k.util.FactorUtil import FactorUtil;
from k.Config import Config;
import  numpy as np;
import pandas as pd;


ONE_YEAR=249;#下标从0开始


#计算是否创造新记录，例如创一年新高
class CreateRecord(Base):


    '''
    isHighOfYear = 'isHighOfYear';  # 是否创一年新高
    isHighOfHistory = 'isHighOfHistor';  # 是否创历史新高
    isLowOfyear = 'isLowOfyear';  # 是否创一年新低
    isLowOfHistory = 'isLowOfHistory';  # 是否创一年新低
    '''
    def _process(self,df,start):

        self.month_data={};

        for i in range(start, df.shape[0], 1):
           '''
           df.loc[i, Config.isHighOfHistory] = 1 \
                if i > 0 and df.loc[i, Config.close] > df.loc[:i - 1,Config.high].max() \
                else 0;
           df.loc[i, Config.isLowOfHistory] = 1 \
                if i > 0 and df.loc[i, Config.close] < df.loc[:i - 1,Config.low].min() \
                else 0;'''
           df.loc[i, Config.isHighOfYear] = 1 \
                if i >= ONE_YEAR and df.loc[i, Config.close] > df.loc[i - ONE_YEAR:i - 1,Config.high].max() \
                else 0;
           df.loc[i, Config.isLowOfyear] = 1 \
                if i >= ONE_YEAR and df.loc[i, Config.close] < df.loc[i - ONE_YEAR:i - 1,Config.low].min() \
                else 0;
           df.loc[i,Config.isMonthReverse]=self.query_month_data_and_count_reverse(df.loc[i,'code'],df.loc[i,Config.db_date],df.loc[i,Config.close])
        return df[[Config.id,Config.isHighOfYear,Config.isLowOfyear,Config.isMonthReverse]]


    def query_month_data_and_count_reverse(self,code,dt,close):

        dt=DateUtil.getLastMonthForShort(dt[0:7]);

        mdf=self.month_data.get(''+code+'_'+dt);
        if( mdf is None):
            mdf=pm.query(DbCreator.share_data_month,where=' code="%s" and trade_date="%s"'%(code,dt));
            self.month_data[code + '_' + dt]=mdf;

        if(not mdf.empty):
            ha=mdf.loc[0,'ha'];
            hb=mdf.loc[0,'hb'];
            if(ha!=0 or  hb!=0):
                #print(ha,hb,ha*12+hb,close)
                if(FactorUtil.is_reverse(ha,hb,close)==1):
                    return 1

            la = mdf.loc[0, 'la'];
            lb = mdf.loc[0, 'lb'];
            if (la != 0 or lb != 0):
                 if (FactorUtil.is_reverse(ha, hb, close,direct='l')==1):
                     return 2;
        return 0;

#main
if (__name__ == '__main__'):
    ONE_YEAR=12;
    cr=CreateRecord();
    df=cr.query_test_data('300394')
    #print(df);
    cr.run('300394',df,start=250,to_mysql=True)


