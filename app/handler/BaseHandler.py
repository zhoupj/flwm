
from app.common.util.LogUtil import logger,digest_log;
from tornado.web import url, RequestHandler;
from app.common.Result import Result;
from app.common.AppException import AppException;
import tornado.web as tw;


class BaseHandler(RequestHandler):
    def set_default_headers(self):

        self.set_header('Access-Control-Allow-Origin','*')
        self.set_header('Access-Control-Allow-Methods','POST, GET')
        self.set_header('Access-Control-Max-Age',1000)
        self.set_header('Access-Control-Allow-Headers','*')
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def post(self, *args, **kwargs):
        #digest_log.info('POST|%s|%s|%s'%(self.request.remote_ip,self.request.full_url,self.request.request_time));
        try:
            dict = {};
            for key in self.request.arguments:
                dict[key] = self.get_arguments(key)[0]
            obj= self.post2(dict);
            self.write(Result.succ(obj))
        except tw.MissingArgumentError as ms:
            logger.exception('MissingArgumentError')
            self.write(Result.fail2(Result.ERROR_PARAM))
        except AppException as ae:
            logger.error('business error,code:%s,err:%s'%(ae.code,ae.err))
            self.write(Result.fail2(ae.info))
        except BaseException as e:
            logger.exception('fail:'+self.__class__.__name__);
            self.write(Result.fail2(Result.ERROR_SYS))

    def post2(self, dict):
        #self.write('网路异常')
        pass


    def get(self, *args, **kwargs):
        try:
            dict = {};
            for key in self.request.arguments:
                dict[key] = self.get_arguments(key)[0]
            self.get2(dict)
        except AppException as ae:
            logger.error('business error,code:%s,err:%s'%(ae.code,ae.err))
            self.write(Result.fail2(ae.info))
        except BaseException as e:
            logger.exception('fail:' + self.__class__.__name__);
            self.write(Result.fail2(Result.ERROR_SYS))

    def get2(self, dict):
        pass

if __name__=='__main__':
    try:
        raise AppException(Result.ERROR_SYS);
    except AppException as b:
        args=b.args;
        print('business error,code:%s,err:%s'%(args[0][0],args[0][1]))