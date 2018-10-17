from k.puller.FinYearPuller import  FinYearPuller;
from k.util.DateUtil import DateUtil;
import  json;
import pandas as pd;
from k.util.SpiderHeaderUtil import SpiderHeaderUtil;
class FinSeasonPuller(FinYearPuller):

    def _get_url(self,code):
        return 'http://emweb.securities.eastmoney.com/PC_HSF10/FinanceAnalysis/MainTargetAjax?code=' \
                  + code + '&type=2';

    def _get_type(self):
        return 1;


if(__name__=='__main__'):
    fp=FinSeasonPuller()
    df =fp.pull('000860',start='2018-06-30',end='2018-06-30',to_mysql=True)
    df.to_csv('f.csv')
    print(df)
