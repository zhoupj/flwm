class Config:
    id='id';
    code='code';
    db_date='trade_date';
    mem_date = 'date';
    open='open';
    high='high';
    low='low';
    close='close';
    volume='volume';#成交量
    turn='turn';#换手率，单位%
    tradestatus='tradestatus';#1：正常，0:停牌
    peTTM='peTTM'#滚动市盈率
    isST='isST';#是否ST
    timeToMarket='timeToMarket';

    totals='totals';#总市值

    isHighOfYear='isHighOfYear';#是否创一年新高
    isHighOfHistory='isHighOfHistory';#是否创历史新高
    isLowOfyear='isLowOfyear';#是否创一年新低
    isLowOfHistory = 'isLowOfHistory';  # 是否创一年新低

    incOfOneYear='incOf250';#一年涨幅，单位%,今日收盘价和250个交易日前的收盘前比较（停牌的不算）
    incOfHalfYear='incOf120';#半年涨幅，单位%，。。。。。120.。。。。。。。。。。。
    incOf50d='incOf50'
    rps120='rps120';# 一年的排名，100－》1
    rps250='rps250';# 半年的排名，100－》1
    rps50='rps50';

    fluOf250d='fluOf250d';#一年的波动幅度，即一年的 （high－low)/high，单位％
    fluOf120d = 'fluOf120d';  # 120日内交易的波动幅度，单位％
    fluOf80d='fluOf80d'; #80日内交易的波动幅度，单位％
    fluOf10d = 'fluOf10d'; # 10日内交易的波动幅度，单位％
    fluOf5d = 'fluOf5d';  # 10日内交易的波动幅度，单位％

    diffToHigh250='diffTohigh250';#距离最高一年的幅度比例，即 (high-close)/close
    diffToHigh120= 'diffTohigh120';#距离半年的幅度比例，即 (high-close)/close
    diffToHigh80 = 'diffTohigh80';  # 距离半年的幅度比例，即 (high-close)/close

    sps120='sps120';#稳定性排名，1/fluOf120d*diffToHigh120，如果创一年新高则换算比例，则diffToHigh120＝(c-cma50)/c
    sps250='sps250';#稳定性排名
    sps80 = 'sps80'

    ma5='ma5';
    ma10='ma10';
    ma20='ma20';
    ma50='ma50';
    ma120='ma120';
    ma250='ma250';

    turn10ma='turn10ma';#10日平均换手率
    turn50ma='turn50ma';#50日平均换手率

    turnIncToYesterDay='turnIncToYesterDay'#相对昨天的换手率比例，单位％
    turnIncTo50Day='turnIncTo50Day'#相对50日平均值的比例，（trun-trun50ma)/trun50ma


    #peS='peS';#静态市盈率
    #peD='peD'#动态市盈率
    curNumPeTTM1Y='curNumPeTTM1Y'#一年中当前市盈率的强度名次
    curNumPeTTM3Y='curNumPeTTM3Y'#三年中
    curNumPeTTM5Y = 'curNumPeTTM5Y';#5年中
    curNumPeTTMALL='curNumPeTTMALL';

    hk_holding_amount='hk_holding_amount';
    hk_holding_ratio='hk_holding_ratio';

