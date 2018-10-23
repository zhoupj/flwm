import datetime;

from k.puller.FinSeasonPuller import FinSeasonPuller;
from k.puller.FinYearPuller import FinYearPuller;
from k.puller.FundsPuller import FundsPuller;
from k.puller.SharePuller import SharePuller;
from k.algorithm.fin.NetProfitMA import NetProfitMA;
from k.algorithm.fin.NetProfitSort import NetProfitSort;
from k.algorithm.fin.NetProfitSort8 import NetProfitSort8;


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
    def count_kpi():
        shp = SharePuller();
        df = shp.query_from_mysql();
        for index, row in df.iterrows():
            code = row['code'];
            nma=NetProfitMA();
            nma.run(code,to_mysql=True,type=1);
        nms = NetProfitSort();
        nms8= NetProfitSort8();
        for dt in['2017-09-30','2017-12-31','2018-03-31','2018-06-30']:
            nms.run(dt,to_mysql=True,type=1)
            nms8.run(dt,to_mysql=True,type=1)


if(__name__=='__main__'):
    FinManager.count_kpi();






