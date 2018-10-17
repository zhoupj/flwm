from k.algorithm.Base import Base;
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

        return df[[Config.id,Config.isHighOfYear,Config.isLowOfyear]]

#main
if (__name__ == '__main__'):
    ONE_YEAR=5;
    nd=np.random.randint(1,100,size=(20,4));
    df=pd.DataFrame(nd,columns=['id','close','low','high'])
    df2=df.copy();
    cr=CreateRecord();
    cr.run('test',df)
    print(df)


    cr.run('test', df2,start=19)
    print(df2)


