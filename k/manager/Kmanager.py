import datetime;
import time;

from k.Config import Config;
from k.algorithm.CreateRecord import CreateRecord;
from k.algorithm.DeviationsRatio import DeviationsRatio;
from k.algorithm.FluctionRatio import FluctionRatio;
from k.algorithm.IncrementRatio import IncrementRatio
from k.algorithm.Ma import Ma;
from k.algorithm.PeRank import PeRank;
from k.algorithm.Pipeline import Pipeline;
from k.algorithm.PreProcess import PreProcess;
from k.algorithm.TurnRatio import TurnRatio;
from k.algorithm.ms.Rps import Rps;
from k.puller.HkHoldPuller import HkHoldPuller;
from k.puller.Kpuller import Kpuller;
from k.puller.SharePuller import SharePuller;
from k.util.DateUtil import DateUtil;
from k.util.DbCreator import DbCreator;
from k.util.Logger import logger;
from k.util.PandasToMysql import pm;
from k.util.PoolManager import PoolManger;

THREAD_NUM=1;

class KManager:

    @staticmethod
    def pull_data(start_date=None):
        plm = PoolManger(THREAD_NUM);

        shp = SharePuller();
        df = shp.query_from_mysql();

        now = datetime.datetime.now()
        end = now.strftime('%Y-%m-%d');

        # 获取基本数据，按列表计算
        for index, row in df.iterrows():
            code = row['code'];
            start = str(row['timeToMarket']);
            if (start_date != None and start < start_date):
                start = start_date;
            # 拉取数据&保存到DB
            kp = Kpuller();
            kp.pull(code, start, end);

        plm.close();

        #获取港资数据
        hkp = HkHoldPuller();
        for dt in DateUtil.getDateSeq(start_date):
            hkp.pull(dt);
            time.sleep(3)


    @staticmethod
    def count_kpi(start_date,s=True,m=True):
        shp = SharePuller();
        df = shp.query_from_mysql();

        end = datetime.datetime.now().strftime('%Y-%m-%d');
        dict = {};

        # ================================
        ## 单指标计算
        # ================================
        if(s):
            for index, row in df.iterrows():
                code = row['code'];
                start = str(row['timeToMarket']);
                if (start_date != None and start < start_date):
                    start = start_date;
                    KManager.kpi_s(code, start_date, pm, dict)
            print('===kpi result======')
            print(dict)

        # ================================
        ## 多指标计算
        # ================================
        if(m):
            if (start_date == None):
                start_date = end;
                KManager.kpi_m(start_date, pm);
            elif (start_date <= end):
                for dt in DateUtil.getDateSeq(start_date):
                    KManager.kpi_m(dt, pm);

    @staticmethod
    def kpi_s(code,start_date,pm,dict):

        df = pm.query(DbCreator.share_data_day, where='code=\'' + code + '\' and trade_date>=\'2011-01-01\'');

        logger.info('start to kpi:'+code+' size:'+str(df.shape[0]));
        #流水线
        succ=Pipeline.execute(PreProcess(),[CreateRecord(),DeviationsRatio(),FluctionRatio(),
                          IncrementRatio(),Ma(),TurnRatio(),PeRank()],code,df,start_date)

        logger.info('end to kpi:'+code)
        dict[code]=succ;

    @staticmethod
    def kpi_m(start_date,pm):
        # 计算跨多只s的指标
        mdf = pm.query(DbCreator.share_data_day, where='trade_date=\'' + start_date + '\'');
        mdf=mdf[[Config.id,Config.incOfOneYear,Config.incOfHalfYear,Config.incOf50d]]
        mdf=mdf.dropna()
        rps = Rps();
        rps.run(mdf,start_date,True);


#main
if (__name__ == '__main__'):
    #pm = PandasToMysql();
    #KManager.kpi_m('2018-09-28',pm)
    p_dt='2018-10-22';
    dt=datetime.datetime.now().strftime('%Y-%m-%d')
    KManager.pull_data(p_dt);
    KManager.count_kpi(p_dt,s=True,m=True);
    #KManager.kpi_m('2018-10-08',PandasToMysql())
