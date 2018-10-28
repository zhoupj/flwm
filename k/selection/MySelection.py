from k.util.PandasToMysql import pm;
import pandas as pd;

class MySelection:
   #hk_holding_amount>3000
    @staticmethod
    def query_by_rps():
        sql='''
        select trade_date,a.code,name,close,rps250,rps120,incOf250,ssr_2,ssr_8,fund_holding,hk_holding_amount,hk_holding_ratio,fluOf250d,fluOf80d,fluOf10d,diffToHigh250,close*c.totals as marketValue,industry from 
            (select * from share_data_day  
             where trade_date='2018-10-25' and (rps250>=87 or rps120>=90)  and diffToHigh250<=12 order by rps250 desc) a
            join 
            (select ssr_2,ssr_8,code,fund_holding from share_data_finance b where b.fin_date='2018-06-30' and b.fin_type=1 and b.fund_holding>3) b
            join 
            (select code,name,totals,industry from share_data_basic) c
            on a.code=b.code 
            and a.code=c.code
            order by diffToHigh250 desc
        '''
        df=pm.query_any(sql)
        return df;

if(__name__=='__main__'):
    pd.set_option('display.width', None)  #解决列之间的省略号
    #pd.set_option('display.max_rows', None) #解决行之间的省略号
    #pd.set_option('display.max_colwidth', 100)
    df=MySelection.query_by_rps();
    print(df)