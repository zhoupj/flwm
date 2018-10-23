from __future__ import unicode_literals
import json;


class Result:

    SUCC=['1000','成功'];
    UKNOWN=['9001','未知异常']

    ERROR_NOT_LOGIN=['1001','未注册'],
    ERROR_EXIST = ['1002', '已经注册'];


    ERROR_URL=['2001','访问路径不存在'],
    ERROR_SYS=['2002','系统繁忙请稍后再试']

    CREATE_MEMBER_FAIL = ['3001', '会员未到期暂不能购买'];


    def __init__(self,succ,data,rst_code=SUCC[0],err_desc='',total=1,pg_size=0):
        self.succ=succ;
        self.data=data;
        self.total=total;
        self.page_size=pg_size;
        self.code=rst_code;
        self.error_desc=err_desc;

    @staticmethod
    def __obj_2_json(obj):
        return {
            "succ":obj.succ,
            "data":obj.data,
            "total":obj.total,
            "page_size":obj.page_size,
            "code":obj.code,
            "err_desc":obj.error_desc
        }

    @staticmethod
    def succ_df(df):
        data='';
        if(df.empty):
            data='';
        else:
            data=df.to_json(orient='records');

        rst = Result(True,data);
        return json.dumps(rst, default=Result.__obj_2_json, ensure_ascii=False);

    @staticmethod
    def succ(obj):
        rst=Result(True,obj);
        return json.dumps(rst,default=Result.__obj_2_json,ensure_ascii=False);

    @staticmethod
    def succ_page(obj,total_count,page_count):
        rst = Result(True, obj,total=total_count,pg_size=page_count);
        return json.dumps(rst,default=Result.__obj_2_json,ensure_ascii=False);

    @staticmethod
    def fail(code,desc):
        rst=Result(False,None,rst_code=code,err_desc=desc)
        return json.dumps(rst,default=Result.__obj_2_json,ensure_ascii=False);

    @staticmethod
    def fail2(enum):
        rst = Result(False, None, rst_code=enum[0], err_desc=enum[1])
        return json.dumps(rst,default=Result.__obj_2_json,ensure_ascii=False);


if(__name__=='__main__'):
    print(Result.succ([23,34,4546]));
    print(Result.succ({"A":"我们等待"}));

