from k.algorithm.Base import Base;
from k.Config import Config;
import  numpy as np;
import pandas as pd;

INC_50=50;#下标从0开始
INC_120=120;
INC_250=250;

#计算增长幅度
class IncrementRatio(Base):
    '''
       incOfOneYear='incOf250d';#一年涨幅，单位%,今日收盘价和250个交易日前的收盘前比较（停牌的不算）
       incOfHalfYear='incOf120d';#半年涨幅，单位%，。。。。。120.。。。。。。。。。。。
       incOf50d='incOf50d'
     '''
    def _process(self,df,start):

        for i in range(start, df.shape[0], 1):
           df.loc[i, Config.incOf50d] = self.__add_increment__(i, INC_50, df);
           df.loc[i, Config.incOfHalfYear] = self.__add_increment__(i, INC_120, df);
           df.loc[i, Config.incOfOneYear] = self.__add_increment__(i, INC_250, df);

        return df[[Config.id,Config.incOfOneYear,Config.incOfHalfYear,Config.incOf50d]]

    def __add_increment__(self, i, freq, df):
        freq = freq - 1;
        if(i>=freq):
            return ((df.loc[i, Config.close] - df.loc[i - freq, Config.close]) / df.loc[i - freq, Config.close]) * 100;
        else:
            return self._default_value;


#main
if (__name__ == '__main__'):
    INC_50=2;
    INC_120=5;
    INC_250=10;
    nd=np.random.randint(1,100,size=(20,3));
    df=pd.DataFrame(nd,columns=['close','low','high'])
    df2=df.copy()
    inR=IncrementRatio();
    inR.run('test',df)
    print(df)

    inR.run('test', df2,start=19)
    print(df2)


