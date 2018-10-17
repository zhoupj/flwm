from k.algorithm.Base import Base;
from k.Config import Config;
import  numpy as np;
import pandas as pd;

#计算均值
class Ma(Base):

    def _process(self,df,start):
        for i in range(start, df.shape[0], 1):
            df.loc[i,Config.ma5]=self.__add_mean__(i,5,df);
            df.loc[i, Config.ma10] = self.__add_mean__(i, 10, df);
            df.loc[i, Config.ma20] = self.__add_mean__(i, 20, df);
            df.loc[i, Config.ma50] = self.__add_mean__(i, 50, df);
            df.loc[i, Config.ma120] = self.__add_mean__(i, 120, df);
            df.loc[i, Config.ma250] = self.__add_mean__(i, 250, df);

        return df[[Config.id,Config.ma5,Config.ma10,Config.ma20,Config.ma50,Config.ma120,Config.ma250]]

    def __add_mean__(self, i, freq, df):
        value = self._default_value;
        freq = freq - 1;
        if (i >= freq):
            value = df.loc[i - freq:i, Config.close].mean();
        return value;


#main
if (__name__ == '__main__'):
    nd=np.random.randint(1,100,size=(20,3));
    df=pd.DataFrame(nd,columns=['close','low','high'])
    df2=df.copy()
    inR=Ma();
    inR.run('test',df)
    print(df)

    inR.run('test', df2,start=19)
    print(df2)


