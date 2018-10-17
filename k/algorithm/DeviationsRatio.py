from k.algorithm.Base import Base ;
from k.Config import Config;
import numpy as np;
import pandas as pd;

D_80 = 80;  # 下标从0开始
D_120 = 120;
D_250 = 250;


# 距离一年新高的差值比例
class DeviationsRatio(Base):
    '''
    diffToHigh250='diffTohigh250';#距离最高一年的幅度比例，即 (high-close)/close
    diffToHigh120= 'diffTohigh120';#距离半年的幅度比例，即 (high-close)/close
    diffToHigh80 = 'diffTohigh80';  # 距离半年的幅度比例，即 (high-close)/close'''
    def _process(self, df, start):
        for i in range(start, df.shape[0], 1):
            df.loc[i, Config.diffToHigh250] = self.__add_deviations__(i, D_250, df);
            df.loc[i, Config.diffToHigh120] = self.__add_deviations__(i, D_120, df);
            df.loc[i, Config.diffToHigh80] = self.__add_deviations__(i, D_80, df);

        return df[[Config.id,Config.diffToHigh250,Config.diffToHigh120,Config.diffToHigh80]]

    def __add_deviations__(self, i, freq, df):
        value = self._default_value;
        freq = freq - 1;
        if (i >= freq):
            value = (df.loc[i - freq:i, Config.high].max() - df.loc[i, Config.close]) / df.loc[i, Config.close];
            value = value * 100;
        return value;


# main
if (__name__ == '__main__'):
    D_80=2;
    D_120=10;
    D_250=15;
    nd = np.random.randint(1, 100, size=(20, 3));
    df = pd.DataFrame(nd, columns=['close', 'low', 'high'])
    df2 = df.copy()
    inR = DeviationsRatio();
    inR.run('test', df)
    print(df)

    inR.run('test', df2, start=19)
    print(df2)


