import pymysql
import pandas as pd
import numpy as np
from sqlalchemy import create_engine;
from k.util.Logger import  Logger;
from k.Config import Config;
'''
need to make sure that the field name in mysql is same with the column name in dataFrame.
'''
class PandasToMysql:

    __use_num=0;
    __instance=None;

    @staticmethod
    #目前未有锁，会有问题
    def instance(host='127.0.0.1',user='root',password='123456',db_name='fin_data'):
        if(PandasToMysql.__instance!=None):
            PandasToMysql.__use_num += 1;
            return PandasToMysql.__instance
        pm=PandasToMysql();
        PandasToMysql.__use_num+=1;
        PandasToMysql.__instance=pm;
        return pm;


    def __init__(self,host='127.0.0.1',user='root',password='123456',db_name='fin_data'):

        try:
            Logger.log('start to connect db...');
            # 打开数据库连接
            self.__conn = pymysql.connect(host, user, password, db_name,charset='utf8');
            self.__cursor=self.__conn .cursor();
            self.__engine = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+db_name+'?charset=utf8')
            Logger.log('connect OK');
        except BaseException as be:
            print('connect to mysql error:',be)


    def create_table(self,sql):
        try:
            self.__cursor.execute(sql);
        except BaseException as be:
            print('create table error:',be)
    #table_name:str type
    #df:DataFrame type，
    #primaryKeys:List type，
    # insert if the primary keys of the record doesn't exist, or update the entire record
    '''
    def save(self,table_name,df,primaryKeys=[Config.code, Config.db_date]):
        
        if(df.empty):
            print('no date to save')
            return
        sql='';
        try:
            #print(df.columns)
            sql='REPLACE INTO '+ table_name + '(' + self.__parse_fields__(df.columns)+ ') values ';
            chip=''
            #for i in np.arange(df.shape[0]):
            for i in df.index:
                chip='('+ self.__parse_values__(df.loc[i,:].values) +')';
                if(i!=df.index[-1]):
                    chip=chip+',';
                sql=sql+chip;
            Logger.log('save sql record count:' + str(df.shape[0]));
            self.__cursor.execute(sql);
            self.__conn.commit();

        except BaseException as be:
            self.__conn.rollback();
            print('save error:',sql,be)
            raise  be;
            # if the updateKyes is None , this method will update all of the columns in the DataFrame df.
    '''
    def save(self, table_name, df, primaryKeys=[Config.code, Config.db_date]):
        if (df.empty):
            print('no date to save')
            return

        exist=[];
        for i in df.index:
            exist.append(self.__query_exist(table_name,df,i,primaryKeys))

        not_exist=list(map(lambda x:not x,exist))
        update_df=df[exist];
        insert_df=df[not_exist]

        Logger.log('save sql record count:' + str(df.shape[0]),'insert',
                   insert_df.shape[0],'update',update_df.shape[0]);


        self.__insert(table_name,insert_df);
        self.update(table_name,update_df,primaryKeys)


    def __query_exist(self,table_name,df,i,primaryKeys):

        sql_prefix='select * from '+table_name+' where ';
        chip = '';
        for vi, val in enumerate(primaryKeys):
            chip += self.__parse_field__(val) + '=' + self.__parse_value__(df.loc[i, val]);
            if (vi < len(primaryKeys) - 1):
                chip = chip + ' and ';
        sql = sql_prefix + chip;
        Logger.log('select *',sql);
        df = pd.read_sql_query(sql, self.__engine);
        if(df.empty):
            return False;
        return True;


    def __insert(self,table_name,df):

        if(df.empty):
            return

        # print(df.columns)
        sql = 'INSERT INTO ' + table_name + '(' + self.__parse_fields__(df.columns) + ') values ';
        chip = ''
        # for i in np.arange(df.shape[0]):
        for i in df.index:
            chip = '(' + self.__parse_values__(df.loc[i, :].values) + ')';
            if (i != df.index[-1]):
                chip = chip + ',';
            sql = sql + chip;
        Logger.log('insert sql record count:' + str(df.shape[0]));
        self.__cursor.execute(sql);
        self.__conn.commit();

    def update(self, table_name, df, primaryKeys):

        if (df.empty):
            print('no date to update')
            return

        try:
            if (primaryKeys == '' or primaryKeys == None):
                raise Exception('primaryKeys is None');
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

                self.__cursor.execute(sql);
            Logger.log('update sql count:'+str(df.shape[0]));
            self.__conn.commit();
        except BaseException as be:
            self.__conn.rollback();
            print('update table error:', be,'sql',sql)
            raise be;

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
        sql='select * from '+table_name ;
        if(where!=None):
            sql=sql+' where '+where;
        Logger.log('select sql:'+sql)
        df = pd.read_sql_query(sql, self.__engine );
        if(index_col!=None):
            df.set_index(index_col,inplace=True)
        return df;

    def close(self):

        if(self==PandasToMysql.__instance):
             PandasToMysql.__use_num-=1;
             if(PandasToMysql.__use_num==0):
                PandasToMysql.__instance.close();
                PandasToMysql.__instance=None;
        else:
            self.__conn.close();



#test
if (__name__ == '__main__'):
     pm=PandasToMysql('127.0.0.1','root','123456','fin_data');
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
     pm.close();

     pm=PandasToMysql.instance();
     pm = PandasToMysql.instance();
     pm.close();
     pm.close();
