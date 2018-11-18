# encoding: utf-8

import baostock as bs
import numpy as np;
import pandas as pd;
import tushare as ts;

from k.Config import Config;
from k.puller.BasePuller import BasePuller;
from k.util.DbCreator import DbCreator;
from k.util.Logger import logger;



bs.login();

class Mpuller(BasePuller):
    def _run(self, code, start, end):
        bs_code = ('sh.' + code) if code[0] == '6' else ('sz.' + code);
        df = self.__pull_kdata_from_baostock_s(bs_code, start, end);
        return df;

    def _save_to_mysql(self, pm, df):
        pm.save(DbCreator.share_data_month, df, primaryKeys=[Config.code, Config.mem_date]);

    def _save_to_csv(self, code, df):
        df.to_csv( code + 'md.csv', mode='w', header=True);

    # pull 2011-01-01  到最新的数据 （执行一次）
    def __pull_kdata_from_baostock_s(self, code, start_date, end_date):

        df = self.__parse_baostock_data(code, start_date, end_date, 'm')

        # parse
        df["id"] = np.arange(df.shape[0]);
        df.set_index('id', inplace=True);
        # code处理
        df['code'] = df['code'].astype(np.str).map(
            lambda x: x[3:]);

        df['date']= df['date'].astype(np.str).map( lambda x:x[0:7]);

        return df;

    # frequency：数据类型，默认为d，日k线；d=日k线、w=周、m=月
    def __parse_baostock_data(self, code, start, end, freq):


        '''
          虽然价格都进行了复权，但是成交量和换手率都没有前复权(tushare和baostock都没做)，同花顺也是， 东方财富做了。
          前复权的价格和同方财富以及同花顺有出入。
        '''
        '''
                能获取2011-01-01至当前时间的数据；
                date	交易所行情日期	格式：YYYY-MM-DD
                code	证券代码	格式：sh.600000。sh：上海，sz：深圳
                open	今开盘价格	精度：小数点后4位；单位：人民币元
                high	最高价	精度：小数点后4位；单位：人民币元
                low	最低价	精度：小数点后4位；单位：人民币元
                close	今收盘价	精度：小数点后4位；单位：人民币元
                preclose	昨日收盘价	精度：小数点后4位；单位：人民币元
                volume	成交数量	单位：股
                amount	成交金额	精度：小数点后4位；单位：人民币元
                adjustflag	复权状态	不复权、前复权、后复权
                turn	换手率	精度：小数点后6位；单位：%
                tradestatus	交易状态	1：正常交易 0：停牌
                pctChg	涨跌幅	精度：小数点后6位
                peTTM	动态市盈率	精度：小数点后4位
                psTTM	市销率	精度：小数点后4位
                pcfNcfTTM	市现率	精度：小数点后4位
                pbMRQ	市净率	精度：小数点后4位
                isST	是否ST	1是，0否'''

        try:
            rs = bs.query_history_k_data(code,
                                     "date,code,open,high,low,close,volume,turn",
                                     start_date=start, end_date=end,
                                     frequency=freq, adjustflag="2")
        except BaseException as e:
            logger.exception('query_history_k_data error');
            raise e
        # print(rs.data);
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        return result;



# test
if (__name__ == '__main__'):
    kp = Mpuller();
    kp.pull('300394', '2016-01-01', '2018-11-30',to_mysql= True,to_csv=False)

