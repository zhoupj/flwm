from app.common.util.DBPool import dbPool;
from app.common.Result import Result;
from app.common.AppException import AppException;
from app.common.util.LogUtil import digest_log,logger;
from app.service.MemberService import MS;
from app.common.util.JsonUtil import JsonUtil;
import  pandas as pd;
import datetime



'''
id int primary key auto_increment,
             open_id varchar(32) not null,
             name varchar(32) not null,
             alias varchar(32)  comment '别名',   
             is_member int default 0  comment '1会员，0不是',
             member_deadline Date comment '会员到期日',
             last_login_time Datetime comment '上一次登录时间',
             login_days int default 0 comment '总共登录天数',
             feature json comment '扩展数据',
             UNIQUE KEY idx_uq_code (open_id)'''

'''
create table if not exists share_buy_record(
             id int primary key auto_increment,
             user_id varchar(8) not null,
             buy_date datetime not null,
             act_id int,
             is_sucess int comment '交易是否成功1是，o否'
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;'''

class UserService:

    __date_col=['member_deadline','last_login_time','this_login_time']
    __TBNAME='share_user';
    __RECORD='share_buy_record';

    def create(self,open_id,name):

        if(not self.__is_exist(open_id)):
            df = pd.DataFrame();
            df.loc[0,'name']=name;
            df.loc[0,'open_id']=open_id;
            df.loc[0,'is_member']=0;
            df.loc[0,'last_login_time']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df.loc[0,'login_days']=1;
            dbPool.insert(UserService.__TBNAME, df);
        else:
            raise AppException(Result.ERROR_EXIST)

    def __is_exist(self,open_id):
        df=dbPool.query_any('select * from %s where open_id="%s"'% (UserService.__TBNAME,open_id));
        if(df.empty):
            return False;
        return True;

    def query(self,open_id):
        df = dbPool.query_any('select * from %s where open_id="%s"' % (UserService.__TBNAME, open_id));
        if(df.empty):
            return {};
        return self.__if_member_expire(df);

    def query_by_id(self, id):
        df = dbPool.query_any('select * from %s where id="%s"' % (UserService.__TBNAME, id));
        if(df.empty):
            return {};
        return self.__if_member_expire(df);

    def is_member(self,id):
        user=self.query_by_id(id);
        if(user and user['is_member']==1):
            return True
        else:
            return False;


    def __if_member_expire(self, df):
        id = df.loc[0, 'id']
        deadline = df.loc[0, 'member_deadline'];

        today = datetime.datetime.now().strftime('%Y-%m-%d');
        if (deadline!=None and today > str(deadline)):
            df.loc[0, 'member_deadline'] = None;
            df.loc[0, 'is_member'] = 0;
            dbPool.execute(
                ['update % set is_member=0 and member_deadline=NULL where id=%d' % (UserService.__TBNAME, id)])
        return JsonUtil.getDict(df,date_col=UserService.__date_col);

    def query_member_detail(self,id):
        buy_df = dbPool.query_any('select * from %s where user_id=%d order by id desc limit 1' % (UserService.__RECORD, id));
        act_id=buy_df.loc[0,'act_id'];
        return MS.query_by_id(act_id);

    def update_login_days(self,id):
        df = dbPool.query_any('select id,login_days,last_login_time from %s where id="%d"' % (UserService.__TBNAME, id));
        df['login_days'] = df ['login_days']+1;
        df['this_login_time']= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        dbPool.update(UserService.__TBNAME,df,primaryKeys=['id'])

    def update_last_login_time(self,id):
        df = dbPool.query_any('select id,last_login_time,this_login_time from %s where id=%d' % (UserService.__TBNAME, id));
        df['last_login_time'] = df['this_login_time']
        dbPool.update(UserService.__TBNAME, df, primaryKeys=['id'])

    def buy_vip(self,user_id,act_id,succ):
        list_sql=[];
        if(succ):
            dead_date=MS.get_deadline_by_id(act_id)
            sql_user='update %s set is_member=1,member_deadline="%s" where id=%s '%(UserService.__TBNAME, dead_date,user_id)
            list_sql.append(sql_user);

        success=1 if succ else 0;
        buy_dt=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        buy_sql='insert into %s (user_id,buy_date,act_id,is_sucess) values (%d,"%s",%d,%d)' %(UserService.__RECORD,user_id,buy_dt,act_id,success)
        list_sql.append(buy_sql);
        dbPool.execute(list_sql);

US=UserService();

if(__name__=='__main__'):
    pd.set_option('display.width', None)  # 解决列之间的省略号
    df=MS.query_all();
    print(df);
    us=UserService();
    #us.create('open_id_test','周来周');
    user=us.query('open_id_test');
    print('--user---')
    id=user['id']
    us.update_last_login_time(id);
    us.update_login_days(id)
    us.buy_vip(id,1,True)
    user=us.query('open_id_test');
    print('user---')
    print(user);