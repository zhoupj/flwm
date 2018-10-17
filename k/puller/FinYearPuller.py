from k.puller.BasePuller import BasePuller ;
import tushare  as ts;
import json;
import pandas as pd;
import numpy as np;
import re;
import requests;
from k.util.DateUtil import  DateUtil;
from k.util.DbCreator import  DbCreator;
from k.util.SpiderHeaderUtil import SpiderHeaderUtil;



class FinYearPuller(BasePuller):



    def _run(self,code,start,end):
        return self.__get_data(code,requests.session())
    '''
    "date":"2018-06-30",
            "jbmgsy":"0.2025",
            "kfmgsy":null,
            "xsmgsy":null,
            "mgjzc":"11.3308",
            "mggjj":"4.9046",
            "mgwfply":"4.5513",
            "mgjyxjl":"1.0685",
            "yyzsr":"32.6亿",
            "mlr":"8.61亿",
            "gsjlr":"1.16亿",
            "kfjlr":"1.16亿",
            "yyzsrtbzz":"20.52",
            "gsjlrtbzz":"103.98",
            "kfjlrtbzz":"102.55",
            "yyzsrgdhbzz":"14.12",
            "gsjlrgdhbzz":"-68.42",
            "kfjlrgdhbzz":"-68.55",
            "jqjzcsyl":null,
            "tbjzcsyl":"1.55",
            "tbzzcsyl":"2.61",
            "mll":"35.62",
            "jll":"3.48",
    '''
    def __get_data(self,code,session):
        code_d = 'sh' + code if code[0] == '6' else 'sz' + code;
        ctx_url = self._get_url(code_d)
        print(ctx_url)
        ctx =session.get(url=ctx_url, headers=SpiderHeaderUtil.get_df_header());
        if (ctx.content != None):
            list = json.loads(ctx.content)['Result'];
            return self._parse(list,code);
        else:
            return None;

    def _get_url(self,code):
        return 'http://emweb.securities.eastmoney.com/PC_HSF10/FinanceAnalysis/MainTargetAjax?code=' \
                  + code + '&type=1';

    def _parse(self,list,code):
        df = pd.DataFrame();
        for idx, obj in enumerate(list):
            df.loc[idx,'code']=code;
            df.loc[idx, 'fin_date']=obj['date'];
            df.loc[idx, 'fin_year'] = DateUtil.getYear(obj['date'])
            df.loc[idx, 'fin_season'] = DateUtil.getSeason(obj['date'])
            df.loc[idx, 'fin_type'] = self._get_type();
            df.loc[idx, 'jll'] = self._filterField(obj['jll']);
            df.loc[idx, 'mll'] = self._filterField(obj['mll'])
            df.loc[idx, 'jbmgsy'] =self._filterField(obj['jbmgsy'])
            df.loc[idx, 'mgjyxjl'] = self._filterField(obj['mgjyxjl'])
            df.loc[idx, 'yyzsr'] = self._filterField(obj['yyzsr'])
            df.loc[idx, 'gsjlr'] = self._filterField(obj['gsjlr'])
            df.loc[idx, 'kfjlr'] = self._filterField(obj['kfjlr'])
            df.loc[idx, 'yyzsrtbzz'] =self._filterField(obj['yyzsrtbzz'])
            df.loc[idx, 'gsjlrtbzz'] = self._filterField(obj['gsjlrtbzz'])
            df.loc[idx, 'kfjlrtbzz'] = self._filterField(obj['kfjlrtbzz'])
        return df;

    def _get_type(self):
        return 0;

    def _filterField(self,value):
        if(value=='--'):
            return None;
        if(u'万' in value):
            return float(re.sub(u'万','',value));
        if (u'亿' in value):
            return float(re.sub(u'亿','',value))*10000;
        return value;


    def _save_to_mysql(self, pm,df):
        pm.save(DbCreator.share_data_finance, df, ['code','fin_year','fin_season','fin_type']);

    def _save_to_csv(self,df):
        return


if(__name__=='__main__'):
    fp=FinYearPuller()
    df =fp.pull('000860',start='2018-06-30',end='2018-06-30',to_mysql=True)
    df.to_csv('f.csv')
    print(df)
