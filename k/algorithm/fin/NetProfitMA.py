

from k.algorithm.fin.FinBase import FinBase;
from k.util.FactorUtil import FactorUtil;


#计算均值
class NetProfitMA(FinBase):

    def _process(self,df):

        df.fillna(method='ffill');

        for i in range(df.shape[0]):
            df.loc[i,'season_ma2']=self.__execute(df,i,2);
            df.loc[i,'season_ma8']=self.__execute(df, i, 8);
        return df;

    def __execute(self,df,i,freq):
       freq=freq-1;
       if(i>=freq):
           return FactorUtil.expma_list(df['gsjlrtbzz'].values[i-freq:i+1])
       else:
           return None;

    def _get_update_df(self,df):
        return df[['id','season_ma2','season_ma8']];



#main
if (__name__ == '__main__'):
    npem=NetProfitMA();
    npem.run('000860',type=1,to_mysql=True)
    lst=[1,2,3,4,5]
    print(lst[1:2])


