# encoding: utf-8
from k.util.PandasToMysql import pm;

#alter table share_data_day modify column fluOf250d double(12,2) DEFAULT NULL COMMENT '250日波动幅度（high-low)/high';

class DbCreator:
    share_base='share_data_basic';
    share_data_day = 'share_data_day';
    share_data_week='share_data_week';
    share_data_month='share_data_month';
    share_data_finance='share_data_finance';
    share_data_month='share_data_month';

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
            is_m_r int comment '1突破月线高点,2突破月线低点,0无',
        
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

    __share_data_month_sql = '''
            create table if not exists share_data_month(
                 id int primary key auto_increment,
                 trade_date char(7) not null comment '2018-10' ,
                 code varchar(6) not null,
                 open double(12,3),
                 high double(12,3),
                 low double(12,3),
                 close double(12,3),
                 volume bigint,
                 turn double(12,3) comment '换手率',
                 ha double(12,3) comment 'y=ax+b 最高价包括自己在内之前12个月',
                 hb double(12,3) comment 'y=ax+b 12个月',
                 la double(12,3) comment 'y=ax+b 最低价包括自己在内之前12个月',
                 lb double(12,3) comment 'y=ax+b 12个月',
                 h_reverse int comment '最高价相当于之前之前12个月是否反转',
                 l_reverse int comment '最低价....',
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
             sb_holding double(12,3) comment '社保基金持有占流通股的比例（%）',
             isExpected int comment '-1 弱于期望，0 正常，1 超出期望',
             season_ma2 double(12,3) comment '最近两个季度净利润增长率的的exma',
             season_ma8 double(12,3) comment '最近10个季度的净利润增长率的exma',
             ssr_2 double(5,2) comment '两个季度排名',
             ssr_8 double(5,2) comment '8个季度排名',
             UNIQUE KEY idx_uq_code (code,fin_year,fin_season,fin_type),
             INDEX idx_y_s (fin_year,fin_season)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    '''

    __share_user_sql='''
        create table if not exists share_user(
             id int primary key auto_increment,
             open_id varchar(32) not null,
             name varchar(32) not null,
             phone char(11),
             email char(64),
             pwd varchar(128),
             is_member int default 0  comment '1会员，0不是',
             member_deadline Datetime comment '会员到期日',
             first_login_time Datetime comment '上一次登录时间',
             last_login_time Datetime comment '第一次登录时间',
             feature text comment '扩展数据',
             UNIQUE KEY idx_uq_code (open_id),
             INDEX idx_code (phone)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    '''

    __share_buy_record='''
         create table if not exists share_buy_record(
             id int primary key auto_increment,
             user_id int not null,
             buy_date datetime not null,
             act_id int,
             is_sucess int comment '交易是否成功1是，o否'
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
         
    __share_member_activity='''
         create table if not exists share_activity(
             
             id int primary key auto_increment,
             act_code varchar(8),
             act_name varchar(16),
             act_desc varchar(128),
             act_state int comment '0失效，1生效',
             amount int comment '单位分'
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;     
        
    '''

    __share_user_sel_sql ='''
        create table if not exists share_user_share_sel(
             id int primary key auto_increment,
             user_id int not null,
             share_code varchar(6) not null,
             add_time datetime not null,
             remove_time datetime,
             inc_flu  double(5,2) comment '增长幅度',
             s_group int comment '股票分组:0 观察 1候选 2 持有3 淘汰',
             tag varchar(500) comment '标记',
             feature text,
             UNIQUE KEY idx_uq_code (user_id,share_code,s_group)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;'''


    __share_trade_record='''
        create table if not exists share_trade_record(
             id int primary key auto_increment,
             user_id int not null,
             share_code varchar(6) not null,
             add_date date not null,
             remove_date date,
             buy_price double(12,2),
             sell_price double(12,2),
             buy_count int default 0,
             yield_rate double(12,2) default 0 comment '收益率',
             actual_yield_rate double(12,2) default 0 comment '实际收益率',
             UNIQUE KEY idx_uq_code (user_id,share_code,add_date)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;

    '''

    __share_article_sql = '''
           create table if not exists share_article(
                id int primary key auto_increment,
                publish_time datetime not null,
                url varchar(512) not null ,
                title varchar(128) not null,
                digest varchar(256) not null,
                ctx text ,
                visit_count int default 0,
                comment_count int default 0,
                feature text
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;
       '''
    
    __alter_sql = '''
           alter table share_data_day modify column open double(12,2) default 0;
           alter table share_data_day modify column  high double(12,2) default 0;
            alter table share_data_day modify column low double(12,2) default 0;
            alter table share_data_day modify column close double(12,2) default 0;
            alter table share_data_day modify column turn double(12,2)  default 0 comment '换手率';
            alter table share_data_day modify column totals double(12,2) default 0 comment '总市值，单位亿';
             
            alter table share_data_day modify column incOf250 double(12,2) default 0 comment '一年的涨幅';
            alter table share_data_day modify column incOf120 double(12,2) default 0, 
            alter table share_data_day modify column incOf50 double(12,2) default 0 ;
            alter table share_data_day modify column incOf2d double(12,2) default 0 ;
            alter table share_data_day modify column rps120 double(5,2) default 0  comment '于同类股比较的涨幅排名';
            alter table share_data_day modify column rps250 double(5,2) default 0 ;
            alter table share_data_day modify column rps50 double(5,2) default 0 ;
        
            alter table share_data_day modify column fluOf250d  double(12,2) default 0  comment '250日波动幅度（high-low)/high';
            alter table share_data_day modify column fluOf120d  double(12,2) default 0 ;
            alter table share_data_day modify column fluOf80d  double(12,2) default 0 ;
            alter table share_data_day modify column fluOf10d double(12,2) default 0 ;
            alter table share_data_day modify column fluOf5d double(12,2) default 0 ;
        
            alter table share_data_day modify column diffToHigh250 double(12,2)  default 0 comment '和一年中最高点距离:（high-close)/high';
            alter table share_data_day modify column diffToHigh120 double(12,2) default 0 ;
            alter table share_data_day modify column diffToHigh80 double(12,2) default 0 ;
        
            alter table share_data_day modify column sps120 double(5,2) default 0  comment '120日安全性排名，值越大，买入的安全性越高，越有潜力';
            alter table share_data_day modify column sps250 double(5,2) default 0 ;
            alter table share_data_day modify column sps80 double(5,2) default 0 ;
        
            alter table share_data_day modify column ma5 double(12,2)  default 0 comment '5日收盘价平均值';
            alter table share_data_day modify column ma10 double(12,2)  default 0 comment '同上';
           alter table share_data_day modify column  ma20 double(12,2) default 0;
            alter table share_data_day modify column ma50 double(12,2) default 0;
            alter table share_data_day modify column ma120 double(12,2) default 0 ;
            alter table share_data_day modify column ma250 double(12,2) default 0 ;
        
            alter table share_data_day modify column turn10ma  double(12,2)  default 0 comment '10日换手率平均值';
            alter table share_data_day modify column turn50ma  double(12,2)  default 0 comment '50日换手率平均值';
        
            alter table share_data_day modify column turnIncToYesterday  double(12,2) default 0 ;
            alter table share_data_day modify column turnIncTo50Day  double(12,2) default 0 ;
        
            alter table share_data_day modify column peTTM double(12,2)  default 0 comment '滚动市盈率';
            alter table share_data_day modify column curNumPeTTM1Y double(12,2)  default 0 comment '滚动市盈率1年中所处位置名次';
            alter table share_data_day modify column curNumPeTTM3Y double(12,2)  default 0 comment '滚动市盈率，3年中';
            alter table share_data_day modify column curNumPeTTM5Y double(12,2)  default 0 comment '滚动市盈率，5年中';
            alter table share_data_day modify column curNumPeTTMALL double(12,2)  default 0 comment '滚动市盈率所有历史';
            
            alter table share_data_day modify column hk_holding_amount double(12,2) default 0  comment '港资持股金额(万）';
            alter table share_data_day modify column hk_holding_ratio double(12,2)  default 0 comment '港资持股比例(%)';
    
           
    
            alter table share_data_finance modify column   fin_date date not null default 0;
              alter table share_data_finance modify column  fin_year int not null comment '2017,2012' default 0;
              alter table share_data_finance modify column  fin_season int not null comment '1,2,2,4' default 0;
              alter table share_data_finance modify column  fin_type int not null comment '0 年度，1 季度 3, 累积' default 0;
              alter table share_data_finance modify column  jll double(12,2) comment '销售净利率(%)' default 0;
              alter table share_data_finance modify column  mll double(12,2) comment '销售毛利率(%)' default 0;
              alter table share_data_finance modify column  jbmgsy double(12,2) comment '每股收益' default 0;
              alter table share_data_finance modify column  mgjyxjl double(12,2) comment '每股经营现金流' default 0;
              alter table share_data_finance modify column  gsjlr double(12,2) comment '归属净利润(万元)' default 0;
              alter table share_data_finance modify column  kfjlr double(12,2) comment '扣费净利润' default 0;
              alter table share_data_finance modify column  yyzsr double(12,2) comment '营业收入' default 0;
              alter table share_data_finance modify column  yyzsrtbzz double(12,2) comment '营业同步增长％' default 0;
              alter table share_data_finance modify column  gsjlrtbzz double(12,2) comment '归属净利润同步增长' default 0;
              alter table share_data_finance modify column  kfjlrtbzz double(12,2) comment '扣非净利润同步增长' default 0;
              alter table share_data_finance modify column  jbmgsytbzz double(12,2) comment '每股收益同步增长' default 0;
              alter table share_data_finance modify column  fund_holding double(12,2) comment '基金持有占流通股的比例（%）' default 0;
              alter table share_data_finance modify column  sb_holding double(12,2) comment '社保基金持有占流通股的比例（%）' default 0;
              alter table share_data_finance modify column  isExpected int comment '-1 弱于期望，0 正常，1 超出期望' default 0;
              alter table share_data_finance modify column  season_ma2 double(12,2) comment '最近两个季度净利润增长率的的exma' default 0;
              alter table share_data_finance modify column  season_ma8 double(12,2) comment '最近10个季度的净利润增长率的exma' default 0;
              alter table share_data_finance modify column  ssr_2 double(5,2) comment '两个季度排名' default 0;
              alter table share_data_finance modify column  ssr_8 double(5,2) comment '8个季度排名'  default 0;
    
    '''

    def init_create_table(self):
        pm.create_table(DbCreator.__share__base_sql);
        pm.create_table(DbCreator.__share_data_day_sql);
        pm.create_table(DbCreator.__share_data_finance_sql);
        pm.create_table(DbCreator.__share_user_sql);
        pm.create_table(DbCreator.__share_user_sel_sql);
        pm.create_table(DbCreator.__share_article_sql);
        pm.create_table(DbCreator.__share_buy_record);
        pm.create_table(DbCreator.__share_member_activity);
        pm.create_table(DbCreator.__share_data_month_sql);
        pm.create_table(DbCreator.__share_trade_record);
       

        print('over')


if (__name__ == '__main__'):
    dc=DbCreator()
    dc.init_create_table();


