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
                    df = df.loc[start:, :];
                    tb_name=self._get_update_table_name();
                    pm.update(tb_name, df, primaryKeys=[Config.id])
                if(to_csv):
                    df.to_csv(code+'-base.csv');

        except Exception  as e:
            logger.exception('base kpi error')
            print(e.__traceback__)
            succ= False;
        digest_log.info('Alg-Base|%s|%s|%d|%s|%s'%(self.__class__.__name__,code,start,to_mysql,succ))
        return  succ;
    
    def _process(self,df,start):
        return;

    def _get_update_table_name(self):
        return DbCreator.share_data_day;

    def query_test_data(self,code,tb_name=DbCreator.share_data_day):
        import numpy as np;
        df= pm.query(tb_name,where ='  code="%s"'%(code));
        df.sort_values(by=[Config.db_date], inplace=True)  # 按列进行排序
        df.index = np.arange(0, df.shape[0], 1)  # 保证索引排序
        df[Config.db_date] = df[Config.db_date].astype(np.str)  # 日期更改
        return df;

