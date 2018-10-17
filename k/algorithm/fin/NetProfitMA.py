

from k.algorithm.fin.FinBase import FinBase;
from k.Config import Config;
import  numpy as np;
import pandas as pd;

#计算均值
class NetProfitMA(FinBase):

    def _process(self,df):

        print(df[['fin_date','gsjlrtbzz']]);






#main
if (__name__ == '__main__'):
    npem=NetProfitMA();
    npem.run('000860',type=1)


