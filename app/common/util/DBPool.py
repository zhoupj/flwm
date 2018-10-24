
#from DBUtils.PooledDB import PooledDB
from app.common.util.LogUtil import logger,digest_log;
import  pymysql;
from sqlalchemy import create_engine;
import  pandas as pd;
from GlobalConfig import ConfigDict;
 

class DBPool:


    def __init__(self, host=ConfigDict['ip'],user=ConfigDict['user'],password=ConfigDict['password'],db_name=ConfigDict['db_name']):

        try:
            logger.info('start to connect db...');
            # 打开数据库连接
            self.__conn = pymysql.connect(host, user, password, db_name, charset='utf8');
            self.__cursor = self.__conn.cursor();
            self.__engine = create_engine(
                'mysql+pymysql://' + user + ':' + password + '@' + host + '/' + db_name + '?charset=utf8')
            logger.info('connect OK');
        except BaseException as be:
            logger.exception('connect to mysql error')

    def save(self, table_name, df, primaryKeys=["code"]):
        if (df.empty):
            logger.info('no data needed to save')
            return
        try:
            exist = [];
            for i in df.index.values:
                exist.append(self.__query_exist(table_name, df, i, primaryKeys))
    
            not_exist = list(map(lambda x: not x, exist))
            update_df = df[exist];
            insert_df = df[not_exist]
    
            logger.debug('save sql record count: %d,insert_count:%d,update_count:%d' %(df.shape[0],
                        insert_df.shape[0],  update_df.shape[0]));
    
            self.insert(table_name, insert_df);
            self.update(table_name, update_df, primaryKeys)
        except Exception as be:
            logger.exception('save  to mysql error:')
            raise be;

    def __query_exist(self, table_name, df, i, primaryKeys):

        sql_prefix = 'select * from ' + table_name + ' where ';
        chip = '';
        for vi, val in enumerate(primaryKeys):
            chip += self.__parse_field__(val) + '=' + self.__parse_value__(df.loc[i, val]);
            if (vi < len(primaryKeys) - 1):
                chip = chip + ' and ';
        sql = sql_prefix + chip;
        logger.debug('select *'+sql);
        df = pd.read_sql_query(sql, self.__engine);
        if (df.empty):
            return False;
        return True;

    def insert(self, table_name, df):

        if (df.empty):
            return

        # print(df.columns)
        sql = 'INSERT INTO ' + table_name + '(' + self.__parse_fields__(df.columns) + ') values ';
        chip = ''
        # for i in np.arange(df.shape[0]):
        for i in df.index.values:
            chip = '(' + self.__parse_values__(df.loc[i, :].values) + ')';
            if (i != df.index[-1]):
                chip = chip + ',';
        sql = sql + chip;
        logger.debug('insert sql record count:' + str(df.shape[0]));
        self.__cursor.execute(sql);
        self.__conn.commit();

    def update(self, table_name, df, primaryKeys):

        if (df.empty):
            logger.info('no date to update')
            return

        try:
            if (primaryKeys == '' or primaryKeys is None):
                raise Exception('primaryKeys is None');
            sql_prefix = 'update ' + table_name + ' set ';

            sql = '';
            # for i in np.arange(df.shape[0]):
            for i in df.index.values:
                chip = '';
                for vi, val in enumerate(df.columns):
                    if (val not in primaryKeys):
                        chip = chip + self.__parse_field__(val) + '=' + self.__parse_value__(df.loc[i, val]);
                        if (vi < len(df.columns) - 1):
                            chip = chip + ','
                if (chip == ''):
                    raise Exception('updated columns is None');
                chip += ' where ';
                for vi, val in enumerate(primaryKeys):
                    chip += self.__parse_field__(val) + '=' + self.__parse_value__(df.loc[i, val]);
                    if (vi < len(primaryKeys) - 1):
                        chip = chip + ' and ';
                sql = sql_prefix + chip;

                self.__cursor.execute(sql);
            logger.debug('update sql count:' + str(df.shape[0]));
            self.__conn.commit();
        except BaseException as be:
            self.__conn.rollback();
            logger.exception('update table error,sql:'+sql)
            raise be;

    def __parse_fields__(self, lst):
        vals = '';
        for i, val in enumerate(lst):
            if (val == 'date'):
                val = 'trade_date';
            if (i < len(lst) - 1):
                vals = vals + str(val) + ','
            else:
                vals += str(val);
        return vals;

    def __parse_field__(self, val):
        if (val == 'date'):
            val = 'trade_date'
        return val;

    def __parse_values__(self, lst):
        vals = '';
        for i, val in enumerate(lst):
            if (i < len(lst) - 1):
                vals = vals + self.__parse_value__(val) + ','
            else:
                vals += self.__parse_value__(val);
        return vals;

    def __parse_value__(self, val):
        if (val == None or val != val or val == 'None' or val == 'nan'):
            return 'NULL';
        return '\'' + str(val) + '\'';


        # 'a>0 and b>0'

    def query(self, table_name, where=None, index_col=None):
        sql = 'select * from ' + table_name;
        if (where != None):
            sql = sql + ' where ' + where;
        logger.debug('select sql:' + sql)
        df = pd.read_sql_query(sql, self.__engine);
        if (index_col != None):
            df.set_index(index_col, inplace=True)
        return df;

        # 'a>0 and b>0'

    def query_any(self, sql, index_col=None):
        logger.debug('select sql:' + sql)
        df = pd.read_sql_query(sql, self.__engine);
        if (index_col != None):
            df.set_index(index_col, inplace=True)
        return df;


    def query_by_req(self,tb_name:str,req_dict:[],resp_lst=None):

        column='*';
        if(resp_lst):
           column=' '.join(resp_lst)+' ';
        cond




    def execute(self,sqls):
        try:
            logger.debug('execute sqls :'+'#'.join(sqls));
            for sql  in sqls:
                self.__cursor.execute(sql);
            self.__conn.commit();
        except BaseException as be:
            self.__conn.rollback();
            logger.exception('execte sql error:')
            raise be;

dbPool=DBPool();

if(__name__=='__main__'):
   df= dbPool.query_any('select * from share_data_basic limit 10');
   print(df)