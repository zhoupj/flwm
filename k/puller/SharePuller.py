# encoding: utf-8

import numpy as np;
import pandas as pd;
import tushare as ts;

from k.Config import Config;
from k.puller.TBasePuller import TBasePuller;
from k.util.DbCreator import DbCreator;
from k.util.PandasToMysql import pm;

'''
Pandas所支持的数据类型: 
1. float 
2. int 
3. bool 
4. datetime64[ns] 
5. datetime64[ns, tz] 
6. timedelta[ns] 
7. category 
8. object （string类型）
默认的数据类型是int64,float64.
'''

CSV_FILE='./data/share.csv';

class SharePuller(TBasePuller):

    def _run(self,dt=None):
        '''
        http://tushare.waditu.com/index.html
        code,代码
        name,名称
        industry,所属行业
        area,地区
        pe,市盈率
        outstanding,流通股本(亿)
        totals,总股本(亿)
        totalAssets,总资产(万)
        liquidAssets,流动资产
        fixedAssets,固定资产
        reserved,公积金
        reservedPerShare,每股公积金
        esp,每股收益
        bvps,每股净资
        pb,市净率
        timeToMarket,上市日期
        undp,未分利润
        perundp, 每股未分配
        rev,收入同比(%)
        profit,利润同比(%)
        gpr,毛利率(%)
        npr,净利润率(%)
        holders,股东人数
        '''
        df = ts.get_stock_basics();
        df = df.loc[:, ['name', 'industry', 'timeToMarket', 'totals', 'outstanding']]
        # 以'id' 为索引
        df.reset_index(inplace=True);
        df["id"] = np.arange(df.shape[0]);
        df.set_index('id', inplace=True);
        # 日期处理
        df['timeToMarket'] = df['timeToMarket'].astype(np.str).map(
            lambda x: pd.NaT if x == '0' else x[0:4] + '-' + x[4:6] + '-' + x[6:8]);
        return df;

    def _save_to_mysql(self, pm,df):
        pm.save(DbCreator.share_base, df, [Config.code]);

    def _save_to_csv(self,df):
        df.to_csv(CSV_FILE, mode='w', header=True, encoding='utf-8');

    def query_from_mysql(self,code=None):
        df=None;
        if(code==None):
            df = pm.query(DbCreator.share_base)
        else:
            df=pm.query(DbCreator.share_data_day,where='code=\''+code+'\'');

        df = df[df[Config.timeToMarket] != '0000-00-00'];
        df=  df.sort_values(by=[Config.code])
        df.index= np.arange(0,df.shape[0],1)

        return df;


#test
if (__name__ == '__main__'):
    df = ts.get_stock_basics();

    df=df.sort_values(by=['code'])
    df.to_csv('s.csv')
    print(df);
