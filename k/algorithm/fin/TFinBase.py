from k.Config import Config;
from k.util.DbCreator import DbCreator;
from k.util.Logger import logger, digest_log;
from k.util.PandasToMysql import pm;


class TFinBase:

    _default_value=None;
    #type:0 年度，1 季度，2 累积 （2暂时无数据）
    def run(self,dt,to_mysql=False,to_csv=False,type=1):

        succ=True;
        try:
            df =self.__query(dt,type);
            df =self._process(df);
            if(to_mysql):
                df=self._get_update_df(df);
                pm.update(DbCreator.share_data_finance,df,primaryKeys=[Config.id])

            if(to_csv):
                df.to_csv(dt+'-fin.csv');

        except Exception  as e:
            logger.exception('fin base error')
            succ= False;

        digest_log.info('TFinBase|%s|%s|%s|%s'%(self.__class__.__name__,dt,to_mysql,succ))
        return succ;

    def __query(self,dt,type):
        df=pm.query(DbCreator.share_data_finance,where=' fin_date=\''+ dt +'\' and fin_type=\''+str(type)+'\' order by fin_date');
        return df;

    def _get_update_df(self,df):
        return df

    def _process(self,df):
        return df




