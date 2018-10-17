from k.algorithm.Base import Base;
from k.Config import Config;
import  numpy as np;
from k.util.DateUtil import DateUtil;
import  pandas as pd;
import  traceback;

class PreProcess:


    def process(self,df,start_data):
        try:
          return (True,self.__process(df,start_data));
        except Exception as e:
            print('pre process error');
            print(e.__traceback__)
            msg = traceback.format_exc()  # 方式1
            print(msg)
            return (False,-1)

    def __process(self,df,start_date):
        df.sort_values(by=[Config.db_date], inplace=True)  # 按列进行排序
        df.index = np.arange(0, df.shape[0], 1)  # 保证索引排序

        start = None;
        if (start_date <=str(df.loc[0, Config.db_date])):
            start= 0;
        elif(start_date >= str( df.loc[df.shape[0]-1,Config.db_date])):
            start=df.shape[0];
        else:
            while(start==None):
                print('while',start,start_date)
                start_v = df[df[Config.db_date] == start_date].index.values;
                if (len(start_v) > 0):
                    start = start_v[0];
                else:
                    start_date=DateUtil.getNextDay(start_date);

        print('start:',start,' start_date:',start_date)
        return start;

#main
if (__name__ == '__main__'):
    df=pd.DataFrame({'trade_date':['2018-10-01','2018-10-03','2018-10-11','2018-09-23'],'code':['a','b','c','d']});
    pre=PreProcess();
    s=pre.process(df,'2018-10-4')
    print(df)
    print(s)
