
from k.util.PandasToMysql import PandasToMysql;
from k.util.PoolManager import PoolManger;
from k.util.DateUtil import DateUtil;
from k.puller.SharePuller import SharePuller;
from k.puller.Kpuller import Kpuller;
from k.puller.HkHoldPuller import  HkHoldPuller;
import datetime;
import time;
from k.puller.FinYearPuller import  FinYearPuller;
from k.puller.FinSeasonPuller import FinSeasonPuller;
from k.puller.FundsPuller import FundsPuller;


class FinManager:

    @staticmethod
    def pull_data():
        shp = SharePuller();
        df = shp.query_from_mysql();

        now = datetime.datetime.now()
        end = now.strftime('%Y-%m-%d');

        for index, row in df.iterrows():
            code = row['code'];
            start = str(row['timeToMarket']);
            #目前start和and 还未生效
            fy = FinYearPuller();
            fy.pull(code, start, end);
            fs = FinSeasonPuller();
            fs.pull(code, start, end);
            fdp = FundsPuller();
            fdp.pull(code, start, end)

    @staticmethod
    def count_kip():
        return;

if(__name__=='__main__'):
    FinManager.pull_data();






#main
if (__name__ == '__main__'):
    main();