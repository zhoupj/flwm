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

class Kpuller(BasePuller):
    def _run(self, code, start, end):
        bs_code = ('sh.' + code) if code[0] == '6' else ('sz.' + code);
        df = self.__pull_kdata_from_baostock_s(bs_code, start, end);
        return df;

    def _save_to_mysql(self, pm, df):
        df = df[df[Config.tradestatus] == '1']
        pm.save(DbCreator.share_data_day, df, primaryKeys=[Config.code, Config.mem_date]);

    def _save_to_csv(self, code, df):
        df.to_csv('../data/' + code + 'kd.csv', mode='w', header=True);

    # pull 2011-01-01  到最新的数据 （执行一次）
    def __pull_kdata_from_baostock_s(self, code, start_date, end_date):

        df = self.__parse_baostock_data(code, start_date, end_date, 'd')
        # parse
        df["id"] = np.arange(df.shape[0]);
        df.set_index('id', inplace=True);
        # code处理
        df['code'] = df['code'].astype(np.str).map(
            lambda x: x[3:]);

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
                                     "date,code,open,high,low,close,volume,turn,tradestatus,peTTM,isST",
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

    # pull 上市日期  到2011-01-01的数据 （执行一次）
    def __pull_kdata_from_tushare(self):
        '''
        date：日期
        open：开盘价
        high：最高价
        close：收盘价
        low：最低价
        volume：成交量
        price_change：价格变动
        p_change：涨跌幅
        ma5：5日均价
        ma10：10日均价
        ma20:20日均价
        v_ma5:5日均量
        v_ma10:10日均量
        v_ma20:20日均量
        turnover:换手率[注：指数无此项]
        '''
        # 遍历取数据，拉取从上市日期到2011-01-04的数据，并补全数据
        sz_df = self.share_list_df;
        print(sz_df.dtypes)
        for index, row in sz_df.iterrows():
            code = row['code'];
            timeToMarket = row['timeToMarket']
            if (
                            timeToMarket == '' or timeToMarket == pd.NaT or timeToMarket != timeToMarket or timeToMarket >= '2011-01-01'):
                continue;
            print('pull data code:' + code + ',date:' + timeToMarket + ',i:' + str(index));

            ts_df = ts.get_k_data(code, start=timeToMarket, end='2011-01-01');  # 前复权数据
            ts_df = ts_df[['date', 'code', 'open', 'high', 'low', 'close', 'volume']];  # chg order
            ts_df[Config.turn] = 0;
            ts_df[Config.tradestatus] = 1;
            ts_df[Config.peTTM] = 0;
            ts_df[Config.isST] = 0;
            ts_df.set_index(['date'], inplace=True)

            # parse and reset index
            '''
                id
                date='date';
                code='code';
                open='open';
                high='high';
                low='low';
                close='close';
                volume='volume';#成交量
                turn='turn';#换手率，单位%
                tradestatus='tradestatus';#1：正常，0:停牌
                peTTM='peTTM'#滚动市盈率
                isST='isST';#是否ST
            '''
            # 选出特定日期的(停牌的数据不要了)
            # fill_ds = KDataGrappler.__szzs_date_serial[KDataGrappler.__szzs_date_serial >= timeToMarket]
            # ts_df=ts_df.reindex(fill_ds)#停牌的数据补充上去
            ts_df = ts_df.reset_index()
            # ts_df["id"] = np.arange(ts_df.shape[0]);
            # ts_df.set_index('id', inplace=True);

            # 读取已有数据
            bs_df = pd.read_csv('./data/' + code + 'kd.csv', dtype=np.str, index_col='id')
            bs_df = bs_df[bs_df['tradestatus'] == '1'];  # 停牌的数据不要了
            # print(bs_df);
            ts_df = pd.concat([ts_df, bs_df], axis=0, ignore_index=True)
            # ts_df=ts_df.append(bs_df)
            ts_df["id"] = np.arange(ts_df.shape[0]);
            ts_df.set_index('id', inplace=True);
            ts_df.to_csv('./data/' + code + 'kd.csv', mode='w', header=True);
            # print(ts_df);
            # 数字格式化
            # print(ts_df.dtypes)
            print('pull data code:' + code + ',date:' + timeToMarket + ',i:' + str(index) + ',end');


# test
if (__name__ == '__main__'):
    kp = Kpuller();
    df = kp.pull('300394', '2016-10-08', '2018-11-25', True)
    print(df)
