

from k.algorithm.fin.TFinBase import TFinBase;
from k.util.SortUtil import SortUtil;


#计算均值
class NetProfitSort(TFinBase):

    def _process(self,df):


        df_2 = df[['id','season_ma2']];
        df_2 = df_2.dropna();
        df_2['ssr_2'] = SortUtil.rank_list(df_2['season_ma2']);
        return df_2;


    def _get_update_df(self,df):
        return df[['id','ssr_2']];



#main
if (__name__ == '__main__'):

    lst=[1,2,3,4,5]
    print(lst[1:2])


