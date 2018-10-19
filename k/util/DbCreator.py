# encoding: utf-8
from k.util.PandasToMysql import  PandasToMysql;
class DbCreator:
    share_base='share_data_basic';
    share_data_day = 'share_data_day';
    share_data_week='share_data_week';
    share_data_month='share_data_month';
    share_data_finance='share_data_finance';

    __share__base_sql='''
        create table if not exists share_data_basic(
             id int primary key auto_increment,
             code varchar(6) not null ,
             name varchar(8) not null,
             industry varchar(10) not null,   
             timeToMarket date ,
             outstanding double(12,3) comment '流通股本(单位亿）',
             totals double(12,3) comment '总股本',
             UNIQUE KEY idx_uq_code (code)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
        ''';

    __share_data_day_sql='''
        create table if not exists share_data_day(
             id int primary key auto_increment,
             trade_date date not null,
             code varchar(6) not null,
             open double(12,3),
             high double(12,3),
             low double(12,3),
             close double(12,3),
             volume bigint,
             turn double(12,3) comment '换手率',
             tradestatus int comment '1 交易，0:停牌',
             isST int ,
             totals double(12,3) comment '总市值，单位亿',
             
            isHighOfYear int comment '收盘价是否创一年新高',
            isHighOfHistory int ,
            isLowOfyear int,
            isLowOfHistory int,
        
            incOf250 double(12,3) comment '一年的涨幅',
            incOf120 double(12,3), 
            incOf50 double(12,3),
            incOf2d double(12,3),
            rps120 double(5,2) comment '于同类股比较的涨幅排名',
            rps250 double(5,2),
            rps50 double(5,2),
        
            fluOf250d  double(12,3) comment '250日波动幅度（high-low)/high',
            fluOf120d  double(12,3),
            fluOf80d  double(12,3),
            fluOf10d double(12,3),
            fluOf5d double(12,3),
        
            diffToHigh250 double(12,3) comment '和一年中最高点距离:（high-close)/high',
            diffToHigh120 double(12,3),
            diffToHigh80 double(12,3),
        
            sps120 double(5,2) comment '120日安全性排名，值越大，买入的安全性越高，越有潜力',
            sps250 double(5,2),
            sps80 double(5,2),
        
            ma5 double(12,3) comment '5日收盘价平均值',
            ma10 double(12,3) comment '同上',
            ma20 double(12,3),
            ma50 double(12,3),
            ma120 double(12,3),
            ma250 double(12,3),
        
            turn10ma  double(12,3) comment '10日换手率平均值',
            turn50ma  double(12,3) comment '50日换手率平均值',
        
            turnIncToYesterday  double(12,3),
            turnIncTo50Day  double(12,3),
        
            peTTM double(12,3) comment '滚动市盈率',
            curNumPeTTM1Y double(12,3) comment '滚动市盈率1年中所处位置名次',
            curNumPeTTM3Y double(12,3) comment '滚动市盈率，3年中',
            curNumPeTTM5Y double(12,3) comment '滚动市盈率，5年中',
            curNumPeTTMALL double(12,3) comment '滚动市盈率所有历史',
            
            hk_holding_amount double(12,3) comment '港资持股金额(万）',
            hk_holding_ratio double(12,3) comment '港资持股比例(%)',
            UNIQUE KEY idx_uq_code (code,trade_date)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    '''

    __share_data_finance_sql='''
        create table if not exists share_data_finance(
             id int primary key auto_increment,
             code varchar(6) not null ,
             fin_date date not null,
             fin_year int not null comment '2017,2012',
             fin_season int not null comment '1,2,3,4',
             fin_type int not null comment '0 年度，1 季度 3, 累积',
             jll double(12,3) comment '销售净利率(%)',
             mll double(12,3) comment '销售毛利率(%)', 
             jbmgsy double(12,3) comment '每股收益', 
             mgjyxjl double(12,3) comment '每股经营现金流',
             gsjlr double(12,3) comment '归属净利润(万元)',
             kfjlr double(12,3) comment '扣费净利润',
             yyzsr double(12,3) comment '营业收入',
             yyzsrtbzz double(12,3) comment '营业同步增长％',
             gsjlrtbzz double(12,3) comment '归属净利润同步增长',
             kfjlrtbzz double(12,3) comment '扣非净利润同步增长',
             jbmgsytbzz double(12,3) comment '每股收益同步增长', 
             fund_holding double(12,3) comment '基金持有占流通股的比例（%）',
             isExpected int comment '-1 弱于期望，0 正常，1 超出期望',
             season_ma2 double(12,3) comment '最近两个季度净利润增长率的的exma',
             season_ma10 double(12,3) comment '最近10个季度的净利润增长率的exma',
             season_strenghth_ranking_2 double(5,2) comment '两个季度排名',
             season_strenghth_rangking_10 double(5,2) comment '10个季度排名',
             UNIQUE KEY idx_uq_code (code,fin_year,fin_season,fin_type),
             INDEX idx_y_s (fin_year,fin_season)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    '''

    def init_create_table(self):
        pm = PandasToMysql();
        pm.create_table(DbCreator.__share__base_sql);
        pm.create_table(DbCreator.__share_data_day_sql);
        pm.create_table(DbCreator.__share_data_finance_sql);
        print('over')


if (__name__ == '__main__'):
    dc=DbCreator()
    dc.init_create_table();