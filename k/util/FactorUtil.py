# -*- coding:utf-8 -*-


'''
Created on 20170709 zhoupj
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class FactorUtil:
    # df pandas.DataFrame,columns='open,high,low,close,volume....'
    # 顺序必须符合上述要求
    # 计算kdj
    @staticmethod
    def kdj(df, days=9, m1=3, m2=3,high='high',low='low',close='close'):
        kdj = pd.DataFrame(index=range(df.index.size), columns=['K', 'D', 'J'])
        print(len(df.values))
        for i in range(len(df.values)):
            if i - days < 0:
                b = 0
            else:
                b = i - days + 1
            block_df = df.iloc[b:i + 1, 0:5]
            RSV = ((block_df.loc[-1, close_idx] - block_df.iloc[:, low_idx].min()) * 1.0 / (block_df.iloc[:, high_idx].max() - block_df.iloc[:, low_idx].min())) * 100
            if i==0:
                K=RSV
                D=RSV
            else:
                K = 1.0/m1 * RSV+(m1-1)*1.0/m1 * K
                D = 1.0/m2 * K+ (m2-1)*1.0/m2 * D
            J = 3 * K - 2 * D
            kdj.iloc[i, 0] = K
            kdj.iloc[i, 1] = D
            kdj.iloc[i, 2] = J
        print (kdj)
        return kdj

    # 计算macd
    @staticmethod
    def macd(df, short=12,long=26,m=9,close_idx=3):
        print(len(df.values))
        macd_df = pd.DataFrame(index=range(df.index.size), columns=['DIF', 'DEA', 'MACD'])
        a=FactorUtil.ema(df,short,close_idx)
        b=FactorUtil.ema(df,long,close_idx)
        #dif
        macd_df.loc[:,'DIF']=a-b
        #dea
        for i in range(macd_df.index.size):
            if(i==0):
                macd_df.iloc[i, 1] = macd_df.iloc[i, 0]
            else:
                macd_df.iloc[i,1]= (2 * macd_df.iloc[i,0] + (m - 1) * macd_df.iloc[i-1, 1]) / (m + 1)
        #macd
        macd_df.iloc[:,2]=2*(macd_df.iloc[:,0]-macd_df.iloc[:,1])
        print (macd_df)
        return macd_df

    @staticmethod
    def ema(df,N,close='close'):
        for i in range(df.shape[0]):
            if i==0:
                df.loc[i,str(N)+'ema']=df.loc[i,close]
            if i>0:
                df.loc[i,str(N)+'ema']=(2*df.loc[i,close]+(N-1)*df.loc[i-1,str(N)+'ema'])/(N+1)
        return df;

    #计算均线
    @staticmethod
    def ma(df,close='close',*args):
        for ct in args:
            for i in range(df.index.size):
                start= (i+1-ct if i+1>=ct else 0)
                end=i
                if(start<end):
                    df.loc[i,str(ct)+'ma']= df.loc[start:end,close].mean();
                else:
                    df.loc[i, str(ct) + 'ma'] = df.loc[start,close];


if __name__ == '__main__':
    df = pd.DataFrame(data=np.random.randint(30,100, size=(100, 5)), columns=['open', 'high', 'low', 'close', 'volume'])
    df.loc[:,'high']=  df.loc[:,'close']+3
    df.loc[:, 'low'] = df.loc[:, 'close'] - 1
    print (df)
    #kdj = get_kdj(df)
    FactorUtil.ma(df,'close',5,30)
    print(df)
    #plt.figure()
    #macd.plot()
    #plt.show()
    exma=FactorUtil.ema(df,8,'close')
    print(exma)


