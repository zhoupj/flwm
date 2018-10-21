from app.common.util.DBPool import dbPool;
from app.common.util.LogUtil import digest_log,logger;
import datetime;
import  pandas as pd;

'''
         create table if not exists share_activity(
             id int primary key auto_increment,
             name varchar(16),
             desc varchar(128),
             act_state int comment '0失效，1生效',
             amount int commnet '单位分',
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;     

    '''

class MemberActivityService:


    @staticmethod
    def query_all():
        return dbPool.query('share_activity',where='act_state=1')

    @staticmethod
    def query_by_id(id):
        return dbPool.query('share_activity',where='id=%d'%(id));

    @staticmethod
    def save_activity(df):
        dbPool.save('share_activity',df,primaryKeys=['act_name']);

    @staticmethod
    def get_deadline_by_id(act_id):
        act_df = dbPool.query_any('select * from share_activity where id=%d' % (act_id));
        act_code = act_df.loc[0, 'act_code'];

        today=datetime.datetime.now();
        dl=today;

        if(act_code=='week_v'):
            dl=today+datetime.timedelta(days=7);
        elif (act_code == 'month_v'):
            dl = today + datetime.timedelta(days=30);
        elif (act_code == 'season_v'):
            dl = today + datetime.timedelta(days=121);
        elif (act_code == 'year_v'):
            dl = today + datetime.timedelta(days=365);

        return dl.strftime('%Y-%m-%d');

if(__name__=='__main__'):
    df=pd.DataFrame();
    idx=0;

    df.loc[idx,'act_state']=1;
    df.loc[idx, 'act_code'] = 'week_v';
    df.loc[idx,'act_name']='周VIP';
    df.loc[idx, 'act_desc'] = '限时五折';
    df.loc[idx, 'amount'] = '1090';

    idx=idx+1;
    df.loc[idx, 'act_state'] = 1;
    df.loc[idx, 'act_code'] = 'month_v';
    df.loc[idx, 'act_name'] = '月度VIP';
    df.loc[idx, 'act_desc'] = '限时五折';
    df.loc[idx, 'amount'] = '3900';

    idx=idx+1;
    df.loc[idx, 'act_state'] = 1;
    df.loc[idx, 'act_code'] = 'season_v';
    df.loc[idx, 'act_name'] = '季度VIP';
    df.loc[idx, 'act_desc'] = '限时五折';
    df.loc[idx, 'amount'] = '12900';

    idx=idx+1;
    df.loc[idx, 'act_state'] = 1;
    df.loc[idx, 'act_code'] = 'year_v';
    df.loc[idx, 'act_name'] = '年度VIP';
    df.loc[idx, 'act_desc'] = '限时五折';
    df.loc[idx, 'amount'] = '42900';

    MemberActivityDO.save_activity(df)