from k.algorithm.Base import Base;
from k.Config import Config;
import  numpy as np;
import pandas as pd;

FLC_80=80;#下标从0开始
FLC_120=120;
FLC_250=250;

#计算增长幅度
class FluctionRatio(Base):
    '''
    fluOf250d='fluOf250d';#一年的波动幅度，即一年的 （high－low)/high，单位％
    fluOf120d = 'fluOf120d';  # 120日内交易的波动幅度，单位％
    fluOf80d='fluOf80day'; #80日内交易的波动幅度，单位％
    fluOf10d = 'fluOf10d'; # 10日内交易的波动幅度，单位％
    fluOf5da = 'fluOf5d';  # 10日内交易的波动幅度，单位％'''
    def _process(self,df,start):
        for i in range(start, df.shape[0], 1):
            df.loc[i, Config.fluOf250d] = self.__add_fluction__(i,FLC_250,df);
            df.loc[i, Config.fluOf120d] = self.__add_fluction__(i, FLC_120, df);
            df.loc[i, Config.fluOf80d] = self.__add_fluction__(i, FLC_80, df);
            df.loc[i, Config.fluOf10d] = self.__add_fluction__(i, 10, df);
            df.loc[i, Config.fluOf5d] = self.__add_fluction__(i, 5, df);
        return df[[Config.id, Config.fluOf250d, Config.fluOf120d, Config.fluOf80d,Config.fluOf10d,Config.fluOf5d]]

    def __add_fluction__(self, i, freq, df):

        freq = freq - 1;  # contain self
        if (i >= freq):
            high = df.loc[i - freq:i, Config.high].max();
            low=df.loc[i - freq:i, Config.low].min();
            return (high -low ) / high *100;
        return self._default_value;


#main
if (__name__ == '__main__'):

    nd=np.random.randint(1,100,size=(20,3));
    df=pd.DataFrame(nd,columns=['close','low','high'])
    df2=df.copy()
    inR=FluctionRatio();
    inR.run('test',df)
    print(df)

    inR.run('test', df2,start=19)
    print(df2)


