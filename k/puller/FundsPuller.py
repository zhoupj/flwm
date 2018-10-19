from k.puller.BasePuller import BasePuller;
import requests;
from copyheaders import headers_raw_to_dict
from k.util.DateUtil import DateUtil;
from k.util.StrUtil import  StrUtil;
from k.util.DbCreator import DbCreator;
import  json;
import  pandas as pd;

post_headers_raw = b'''
Accept:*/*
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9
Cache-Control:no-cache
Connection:keep-alive
DNT:1
Host:emweb.securities.eastmoney.com
Pragma:no-cache
Referer:http://emweb.securities.eastmoney.com/FinanceAnalysis/Index?type=web&code=sh603180
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
X-Requested-With:XMLHttpRequest
'''
# 把header转化为字典类型
header_dict = headers_raw_to_dict(post_headers_raw)

class FundsPuller(BasePuller):


    def _run(self,code,start,end):
        ss=requests.session();
        code_d='sh'+code if code[0]=='6' else 'sz'+code;
        f_data_list=[];
        # 得到日期
        url = 'http://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/ShareholderResearchAjax?code=' + code_d;
        ctx = ss.get(url=url, headers=header_dict);
        if (ctx.content != None):
            f_data_list = json.loads(ctx.content)['zlcc_rz'];
            print('funds date:',f_data_list)

        df=pd.DataFrame();
        for idx,f_d in enumerate(f_data_list):
            url = 'http://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/MainPositionsHodlerAjax?date='+ str(f_d)+'&code='+code_d;
            print(url)
            ctx = ss.get(url=url, headers=header_dict);
            df.loc[idx,'code']=code;
            df.loc[idx,'fin_year']=DateUtil.getYear(f_d);
            df.loc[idx,'fin_season']=DateUtil.getSeason(f_d);
            df.loc[idx,'fin_type']=1;
            if(ctx.content!=None):
                data_list= json.loads(ctx.content);
                for d in data_list:
                    if(d['jglx']==u'基金'):
                        df.loc[idx,'fund_holding']=StrUtil.parse_field(d['zltgbl']);


        return df;

    def _save_to_mysql(self,pm,df):
        pm.update(DbCreator.share_data_finance, df, ['code', 'fin_year', 'fin_season', 'fin_type']);

if(__name__=='__main__'):
    fp=FundsPuller()
    df =fp.pull('000691',start='2018-06-30',end='2018-06-30',to_mysql=True)
    print(df)
