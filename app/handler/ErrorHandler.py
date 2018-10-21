from app.common.util.LogUtil import digest_log,logger,suggest_log;
from tornado.web import url, RequestHandler;
from app.common.Result import Result;

class ErrorHandler(RequestHandler):

    def post(self, *args, **kwargs):
        try:

            self.write(Result.fail2(Result.ERROR_URL))
        except Exception as e:
            logger.exception('fail');
            self.write(Result.fail2(Result.ERROR_SYS))
