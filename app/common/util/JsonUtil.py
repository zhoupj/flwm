#encoding=utf-8
import  pandas as pd;
import json
import datetime;
import numpy as np;



class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class JsonUtil:

    @staticmethod
    def getDict(df,date_col=[]):
         if( df is None or df.empty ):
             return {}
         df=df=JsonUtil.__parse_dt(df,date_col);
         str_ls= df.to_json(orient='records');
         lst=json.loads(str_ls,encoding='utf-8');
         return lst[0];

    @staticmethod
    def getList(df,date_col=[]):
        if( df is None or df.empty):
            return [];
        df = df = JsonUtil.__parse_dt(df, date_col);
        str_ls = df.to_json(orient='records',date_format='%Y-%m-%d');
        lst = json.loads(str_ls,encoding='utf-8');

        return lst;

    @staticmethod
    def __parse_dt(df,date_col):
        cols=df.columns.values;
        if(date_col):
            for col in date_col:
                if(col in cols):
                    df[col] = df[col].astype(np.str)  # 日期更改

        return df;
if(__name__=='__main__'):
    df = pd.DataFrame(data={'Num': [1, 2, 3], 'char': ['a', '我', 'c']})
    print(JsonUtil.getDict(df))
    print(JsonUtil.getList(df))
    print(JsonUtil.getList(None))
    print(JsonUtil.getDict(pd.DataFrame()))