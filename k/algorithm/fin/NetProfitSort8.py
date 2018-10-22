

from k.algorithm.fin.TFinBase import TFinBase;
from k.util.SortUtil import SortUtil;


#计算均值
class NetProfitSort8(TFinBase):

    def _process(self,df):

        df_8=df[['id','season_ma8']];
        df_8=df_8.dropna();
        df_8['ssr_8'] = SortUtil.rank_list(df_8['season_ma8']);
        return df_8;


    def _get_update_df(self,df):
        return df[['id','ssr_8']];


#main
if (__name__ == '__main__'):

    lst=[1,2,3,4,5]
    print(lst[1:2])


