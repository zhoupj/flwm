

from k.puller.TBasePuller import TBasePuller;
from k.Config import  Config;
import requests
import re
import json
import  pandas as pd;
from copyheaders import headers_raw_to_dict
import  datetime;
from k.util.Logger import Logger;
from k.util.StrUtil import StrUtil;
from k.util.PandasToMysql import PandasToMysql;
from k.util.DbCreator import DbCreator;

post_headers_raw=b'''
Accept:*/*
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9
Cache-Control:no-cache
Connection:keep-alive
DNT:1
Host:dcfm.eastmoney.com
Pragma:no-cache
Referer:http://data.eastmoney.com/hsgtcg/StockStatistics.aspx
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
X-Requested-With:XMLHttpRequest
'''
#把header转化为字典类型
header_dict= headers_raw_to_dict(post_headers_raw)


request_get_raw='''
type: HSGTHDSTA
token: 70f12f2f4f091e459a279469fe49eca5
st: HDDATE,SHAREHOLDPRICE
sr: 3
p: 1
ps: 50
js: var LIkffNKM={pages:(tp),data:(x)}
filter: (MARKET in ('001','003'))(HDDATE=^2018-10-12^)
rt: 51317778
'''
#params_dict = headers_raw_to_dict(request_get_raw)
params_dict=StrUtil.convert_to_dict(request_get_raw);

class HkHoldPuller(TBasePuller):

    def _run(self,dt=None):

        df = self.__get_data(dt);

        if(df.empty):
            print('pull hk but no date ')
            return df;

        return df;

    def _save_to_mysql(self, pm,df):
        pm.update(DbCreator.share_data_day, df, primaryKeys=[Config.code, Config.db_date]);

    def _save_to_csv(self,df):
        df.to_csv('../log/hk-holding.csv');

    def __get_data(self,dt):

        if(dt==None):
            dt=datetime.datetime.now().strftime('%Y-%m-%d');

        params_dict['filter']=params_dict['filter'].replace('2018-10-12',dt);

        # 构造session ，用于存储browser和server交互之间的cookie
        self.session = requests.session();
        # 任意相关url
        init_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get';
        ctx = self.session.get(url=init_url,params=params_dict, headers=header_dict);
        print(ctx.url)
        # print 'ctx:'+ctx.content;
        # print(ctx.headers)
        # print(ctx.cookies)
        tp=self.__parse(ctx);

        df=pd.DataFrame();
        i=0;

        for p in range(1,tp[0],1):
            Logger.log("request page no:",p)
            params_dict['p']=p;

            ctx = self.session.get(url=init_url, params=params_dict, headers=header_dict);
            tp=self.__parse(ctx);
            lst=tp[1];
            #print(lst)
            for obj in lst:
                df.loc[i,Config.code]=obj['SCODE']
                df.loc[i,Config.db_date]=dt;
                df.loc[i,Config.hk_holding_amount]=obj['SHAREHOLDPRICE']/10000.0;
                df.loc[i,Config.hk_holding_ratio]=obj['SHARESRATE'];
                i=i+1;

        if(i==0):
            return df;
        df.sort_values(by=[Config.hk_holding_ratio],inplace=True,ascending=False)
        return df;

    def __parse(self,ctx):
        index = ctx.text.find('{');
        json_text = ctx.text[index:]
        json_text = json_text.replace('pages', '\"pages\"');
        json_text = json_text.replace('data', '\"data\"')
        jl = json.loads(json_text)
        pages = int(jl['pages']);
        list = jl['data']
        return (pages,list);

if(__name__=='__main__'):
    hp=HkHoldPuller();
    df=hp.pull('2018-10-18',to_mysql=True)
    print(df)