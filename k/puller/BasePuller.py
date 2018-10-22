from k.util.Logger import logger,digest_log;
from k.util.PandasToMysql import pm;


class BasePuller:

    def pull(self,code:str,start:str,end:str,to_mysql=True,to_csv=False):
        succ=True;
        df=None;
        try:
           df= self._run(code,start,end);
           if(to_mysql):
                self._save_to_mysql(pm,df);
           if(to_csv):
                self._save_to_csv(code,df)
        except Exception as e:
            logger.exception('puller error')
            succ=False;

        digest_log.info('puller|%s|%s|%s|%s|%s|%s'%(self.__class__.__name__,code,start,end,str(to_mysql),succ))
        return df;

    def _run(self,code,start,end):
        return;

    def _save_to_mysql(self,pm,df):
        return

    def _save_to_csv(self,code,df):
        return


    def query(self,code=None,start=None,end=None):
        return;