import numpy as np;
import pandas as pd;

from k.Config import Config;
from k.algorithm.ms.MultiBase import MultiBase;
from k.util.SortUtil import SortUtil;


class Rps(MultiBase):

    def _process(self, df):
        df[Config.rps250]=SortUtil.rank_list(df[Config.incOfOneYear]);
        df[Config.rps120]=SortUtil.rank_list(df[Config.incOfHalfYear]);
        df[Config.rps50]=SortUtil.rank_list(df[Config.incOf50d]);

        return df[[Config.id,Config.rps120,Config.rps250,Config.rps50]]

#main
if (__name__ == '__main__'):

    nd=np.random.randint(1,200,size=(500,5));
    df=pd.DataFrame(nd,columns=['id','code',Config.incOfOneYear,Config.incOfHalfYear,Config.incOf50d])
    df2=df.copy()
    inR=Rps();
    inR.run(df,'2018-01-01',to_mysql=False)
    print(df)

