#import pymysql
import pandas as pd
import numpy as np
#from sqlalchemy import create_engine;
from k.util.Logger import logger,digest_log;
from k.Config import Config;
from GlobalConfig import ConfigDict;
import mysql.connector.pooling
#pymysql.install_as_MySQLdb()



'''
need to make sure that the field name in mysql is same with the column name in dataFrame.
'''


class PandasToMysql:

    __use_num=0;
    __instance=None;

    def __init__(self,host=ConfigDict['ip'],user=ConfigDict['user'],password=ConfigDict['password'],db_name=ConfigDict['db_name']):

        try:
            logger.info('start to build pool');
            self.pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, host=host,
                                                                     port=3306, database=db_name,
                                                                     user=user, password=password,
                                                                     pool_reset_session=True)


            # self.pool = pool = ConnectionPool(**config);
            #     PooledDB(MySQLdb, mincached=5,maxcached=5, maxconnections=20, host='localhost', user='root', passwd='pwd', db='myDB', port=3306)
            # # 打开数据库连接
            #self.__conn = pymysql.connect(host, user, password, db_name,charset='utf8');
            #self.__cursor=self.__conn .cursor();
            #self.__engine = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+db_name+'?charset=utf8')
            logger.info('build pool OK');
        except BaseException as be:
            logger.exception('build  error');
            raise  be;


    def create_table(self,sql):
        conn = self.pool.get_connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
        cur = conn.cursor()
        try:
            cur.execute(sql);
        except BaseException as be:
            print('create table error:',be)
        finally:
            cur.close()
            conn.close()


    def save(self, table_name, df, primaryKeys=[Config.code, Config.db_date]):
        if (df.empty):
            logger.info('no data to save ')
            return

        exist=[];
        for i in df.index:
            exist.append(self.__query_exist(table_name,df,i,primaryKeys))

        not_exist=list(map(lambda x:not x,exist))
        update_df=df[exist];
        insert_df=df[not_exist]

        logger.info('save db count:%d,insert %d,update:%d'%(df.shape[0],insert_df.shape[0],update_df.shape[0]))

        self.__insert(table_name,insert_df);
        self.update(table_name,update_df,primaryKeys)


    def __query_exist(self,table_name,df,i,primaryKeys):

        conn=self.get_conn();
        try:
            sql_prefix='select * from '+table_name+' where ';
            chip = '';
            for vi, val in enumerate(primaryKeys):
                chip += self.__parse_field__(val) + '=' + self.__parse_value__(df.loc[i, val]);
                if (vi < len(primaryKeys) - 1):
                    chip = chip + ' and ';
            sql = sql_prefix + chip;
            #logger.debug('select *'+sql);
            df = pd.read_sql_query(sql, conn);
            if(df.empty):
                return False;
            return True;
        finally:
            conn.close()



    def __insert(self,table_name,df):

        if(df.empty):
            return

        conn = self.get_conn();
        cur = conn.cursor();

        try:
            # print(df.columns)
            sql = 'INSERT INTO ' + table_name + '(' + self.__parse_fields__(df.columns) + ') values ';
            chip = ''
            # for i in np.arange(df.shape[0]):
            for i in df.index:
                chip = '(' + self.__parse_values__(df.loc[i, :].values) + ')';
                if (i != df.index[-1]):
                    chip = chip + ',';
                sql = sql + chip;
            logger.debug('insert sql record count:' + str(df.shape[0]));

            cur.execute(sql);
            conn.commit();

        finally:
            cur.close();
            conn.close();

    def update(self, table_name, df, primaryKeys):

        if (df.empty):
            logger.info('no date to update')
            return

        if (primaryKeys == '' or primaryKeys == None):
            raise Exception('primaryKeys is None');

        conn = self.get_conn();
        cur = conn.cursor();
        try:

            sql_prefix = 'update ' + table_name + ' set ';
            sql='';
            #for i in np.arange(df.shape[0]):
            for i in df.index:
                chip = '';
                for vi, val in enumerate(df.columns):
                    if(val not in primaryKeys):
                        chip =chip+ self.__parse_field__(val) + '=' + self.__parse_value__(df.loc[i, val]);
                        if (vi < len(df.columns) - 1):
                            chip = chip + ','
                if(chip==''):
                    raise Exception('updated columns is None');
                chip += ' where ';
                for vi, val in enumerate(primaryKeys):
                    chip += self.__parse_field__(val) + '=' + self.__parse_value__(df.loc[i, val]);
                    if (vi < len(primaryKeys) - 1):
                        chip = chip + ' and ';
                sql = sql_prefix + chip;
                cur.execute(sql);
            logger.debug('update sql count:'+str(df.shape[0]));
            conn.commit();
        except BaseException as be:
            conn.rollback();
            logger.exception('updat db error')
            raise be;
        finally:
            cur.close();
            conn.close();

    def __parse_fields__(self,lst):
        vals='';
        for i,val in enumerate(lst):
            if(val=='date'):
                val='trade_date';
            if(i<len(lst)-1):
                vals=vals+str(val)+','
            else:
                vals+=str(val);
        return vals;

    def __parse_field__(self,val):
        if(val=='date'):
            val='trade_date'
        return val;

    def __parse_values__(self,lst):
        vals='';
        for i,val in enumerate(lst):
            if(i<len(lst)-1):
                vals=vals+self.__parse_value__(val)+','
            else:
                vals+=self.__parse_value__(val);
        return vals;

    def __parse_value__(self,val):
        if( val==None or val!=val or val=='None' or val=='nan' ):
            return 'NULL';
        return '\'' + str(val) + '\'';


    # 'a>0 and b>0'
    def query(self,table_name,where=None,index_col=None):

        conn=self.get_conn();
        try:
            sql='select * from '+table_name ;
            if(where!=None):
                sql=sql+' where '+where;
            logger.debug('select sql:'+sql)
            df = pd.read_sql_query(sql, conn);
            if(index_col!=None):
                df.set_index(index_col,inplace=True)
            return df;
        finally:
            conn.close();

    # 'a>0 and b>0'
    def query_any(self, sql, index_col=None):
        conn = self.get_conn();
        try:
            logger.debug('select sql:' + sql)
            df = pd.read_sql_query(sql, conn);
            if (index_col != None):
                df.set_index(index_col, inplace=True)
            return df;
        finally:
            conn.close();

    # def close(self):
    #     print('db close')
    #     if(self==PandasToMysql.__instance):
    #          PandasToMysql.__use_num-=1;
    #          if(PandasToMysql.__use_num==0):
    #             PandasToMysql.__instance.close();
    #             PandasToMysql.__instance=None;
    #     else:
    #         self.__conn.close();
    def get_conn(self):
        return self.pool.get_connection();
pm=PandasToMysql();

#test
if (__name__ == '__main__'):
     #pm=PandasToMysql('127.0.0.1','root','123456','fin_data');
     create_table_sql='''
         create table IF NOT EXISTS tb_emp (
             id int primary key auto_increment,
             Name varchar(18),
             sex varchar(2),
             age int,   
             address varchar(200),
             email varchar(100),
             birthday date,
             high double(16,2),
             UNIQUE KEY idx_uq_name_age (Name,age)
         )ENGINE=InnoDB DEFAULT CHARSET=utf8;''';
     pm.create_table(create_table_sql)

     df=pd.DataFrame({'Name':['zhou','piao','tttt'],
                      'age':[23,34,902],
                      'sex': ['1', '0','1'],
                      'address':['where','here','that'],
                      'email':['qqq','qq','wx'],
                      'birthday':['2018-09-09','2019-09-01','2019-09-09'],
                      'high':[23444.4451,46444.23455,4]});
     print(df);
     #pm.save_new('tb_emp',df);
     # df = pm.query('tb_emp', 'age>10');
     # print(df);
     # df=df[['Name','age','high']];
     # df.loc[0,'high']=None;
     # print(df);
     pm.save('tb_emp',df,primaryKeys=['Name','age']);
     df=pm.query('tb_emp','age>10');
     print(df.dtypes)
     print(df);

     df=pm.query_any('select * from share_data_day where code=\'000860\' order by trade_date desc limit 20');
     print(df);
     df[Config.db_date] = df[Config.db_date].astype(np.str)
     print(df.dtypes)
     print(df[df[Config.db_date]=='2018-10-15'].index.values[0]);
     print(df.loc[1:,])
