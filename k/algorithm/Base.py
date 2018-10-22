from k.Config import Config;
from k.util.DbCreator import DbCreator;
from k.util.Logger import logger, digest_log;
from k.util.PandasToMysql import pm;


class Base:

    _default_value=None;

    def run(self,code,df,start=0,to_mysql=False,to_csv=False):

        succ=True;
        try:
            if (df.empty or df.shape[0] == 0):
                logger.info('no date to count kpi');
            else:
                df=self._process(df,start);

                if(to_mysql):
                    df=df.loc[start:,:];
                    pm.update(DbCreator.share_data_day,df,primaryKeys=[Config.id])
                if(to_csv):
                    df.to_csv(code+'-base.csv');

        except Exception  as e:
            logger.exception('base kpi error')
            succ= False;
        digest_log.info('Alg-Base|%s|%s|%d|%s|%s'%(self.__class__.__name__,code,start,to_mysql,succ))
        return  succ;
    
    def _process(self,df,start):
        return;




