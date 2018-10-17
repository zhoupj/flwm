from k.algorithm.Base import Base;
from k.Config import Config;
import  numpy as np;
import pandas as pd;


TURN_10=10;
TURN_50=50;

#计算换手率
class TurnRatio(Base):
    '''
       turn10ma='turn10ma';#10日平均换手率
       trun50ma='turn50ma';#50日平均换手率
       turnIncToYesterDay='turnIncToYesterDay'#相对昨天的换手率比例，单位％
       turnIncTo50Day='turnIncTo50Day'#相对昨天50日平均值的比例，（trun-trun50ma)/trun50ma
       '''
    def _process(self,df,start):
        for i in range(start, df.shape[0], 1):
            df.loc[i, Config.turn10ma] = self.__add_turn__(i, TURN_10, df);
            df.loc[i, Config.turn50ma] = self.__add_turn__(i, TURN_50, df);

            if(i>=TURN_10):
                df.loc[i,Config.turnIncToYesterDay]=(df.loc[i, Config.turn]-df.loc[i-1, Config.turn])/df.loc[i-1, Config.turn]*100;
            else:
                df.loc[i, Config.turnIncToYesterDay]=self._default_value;

            if(i>=TURN_50):
                df.loc[i, Config.turnIncTo50Day] = (df.loc[i, Config.turn] - df.loc[i , Config.turn50ma]) / \
                                                       df.loc[i, Config.turn50ma] * 100;
            else:
                df.loc[i, Config.turnIncTo50Day]=self._default_value;
        return df[[Config.id,Config.turn10ma,Config.turn50ma,Config.turnIncToYesterDay,Config.turnIncTo50Day]]

    def __add_turn__(self, i, freq, df):
        value = self._default_value;
        freq = freq - 1;
        if (i >= freq):
            value = df.loc[i - freq:i, Config.turn].mean();
        return value;


#main
if (__name__ == '__main__'):
    TURN_50=10;
    TURN_10=5;
    nd=np.random.randint(1,100,size=(20,2));
    df=pd.DataFrame(nd,columns=['close','turn'])
    df2=df.copy()
    inR=TurnRatio();
    inR.run('test',df)
    print(df)

    inR.run('test', df2,start=19)
    print(df2)



