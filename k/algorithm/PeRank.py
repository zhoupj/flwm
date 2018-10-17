from k.algorithm.Base import Base;
from k.Config import Config;
import  numpy as np;
import pandas as pd;
from k.util.SortUtil import SortUtil;

PER_1Y=250;#下标从0开始
PER_2Y=500;
PER_3Y=750;


#计算市盈率名次
class PeRank(Base):
    '''
    curNumPeTTM1Y='curSpeTTM1Y'#一年中当前市盈率的强度名次
    curNumPeTTM3Y='curSpeTTM3Y'#三年中
    curNumPeTTM5Y='curSpeTTM5Y';#5年中
    curNumPeTTMALL='curNumPeTTMALL';
    '''
    def _process(self,df,start):

        for i in range(start, df.shape[0], 1):
            df.loc[i, Config.curNumPeTTM1Y] = self.__add_pe_ranking__(i, PER_1Y, df);
            df.loc[i, Config.curNumPeTTM3Y] = self.__add_pe_ranking__(i, PER_2Y, df);
            df.loc[i, Config.curNumPeTTM5Y] = self.__add_pe_ranking__(i, PER_3Y, df);
            # df.loc[i, Config.curNumPeTTMALL] = self.__add_pe_ranking__(i, 1, df);

        return df[[Config.id,Config.curNumPeTTM1Y,Config.curNumPeTTM5Y,Config.curNumPeTTM3Y]]

    def __add_pe_ranking__(self, i, freq, df):
        # 1-100排名，如果重复则取均值
        freq = freq - 1;
        if (i < freq):
            return self._default_value;

        start = i - freq;
        if (freq == -1):
            start = 0;
        return SortUtil.rank(df.loc[start:i, Config.peTTM]);


#main
if (__name__ == '__main__'):
    PER_1Y=10;
    PER_2Y=200;
    PER_3Y=250;
    nd=np.random.randint(1,100,size=(500,2));
    df=pd.DataFrame(nd,columns=['close','peTTM'])
    df2=df.copy()
    inR=PeRank();
    inR.run('test',df)
    print(df)

    inR.run('test', df2,start=19)
    print(df2)


