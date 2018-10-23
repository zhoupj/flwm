
from app.common.util.LogUtil import logger;
from tornado.web import url, RequestHandler;
from app.common.Result import Result;


class BaseHandler(RequestHandler):
    def set_default_headers(self):

        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def post(self, *args, **kwargs):
        try:
            self.post2(args,kwargs);
        except Exception as e:
            logger.exception('fail:'+self.__class__.__name__);
            self.write(Result.fail2(Result.ERROR_SYS))

    def post2(self, *args, **kwargs):
        self.write('网路异常')


    def get(self, *args, **kwargs):
        try:
            self.get2(args, kwargs)
        except Exception as e:
            logger.exception('fail:' + self.__class__.__name__);
            self.write(Result.fail2(Result.ERROR_SYS))

    def get2(self, *args, **kwargs):
        self.write('网路异常')