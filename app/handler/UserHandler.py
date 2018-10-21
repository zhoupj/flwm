from app.common.util.LogUtil import digest_log,logger,suggest_log;
from tornado.web import url, RequestHandler;
from app.common.Result import Result;
from app.service.UserService import UserService;
from app.service.MemberActivityService import  MemberActivityService;

US = UserService();

class Register(RequestHandler):
    def post(self, *args, **kwargs):
        try:
            # 暂时用openId，当作code，之后要改造
            code = self.post_argument("code");
            name = self.post_argument("name");

            # 调用微信接口换取openId
            # TODO
            open_id = code;
            US.create(open_id,name);
            df=US.query(open_id);
            self.write(Result.succ(df.to_json(orient='records')))
        except Exception as e:
            logger.exception('fail');
            self.write(Result.fail2(Result.CREATE_USER_FAIL))

class Login(RequestHandler):
    def post(self, *args, **kwargs):
        try:
            code = self.post_argument('code');
            df = US.query(code);
            US.update_login_days(df.loc[0,'id']);
            self.write(Result.succ(df.to_json(orient='records')))
        except Exception as e:
            logger.exception('fail');
            self.write(Result.fail(Result.ERROR_SYS))

class Quit(RequestHandler):
    def post(self, *args, **kwargs):
        try:
            id =int(self.post_argument('user_id'));
            df = US.query_by_id(id)
            US.update_last_login_time(id);
            self.write(Result.succ('udpate sucess'));
        except Exception as e:
            logger.exception('fail');
            self.write(Result.fail2(Result.ERROR_SYS))

class MemberActivity(RequestHandler):
    def post(self, *args, **kwargs):
        try:
            df = MemberActivityService.query_all();
            self.write(Result.succ(df.to_json(orient='records')));
        except Exception as e:
            logger.exception('fail');
            self.write(Result.fail2(Result.ERROR_SYS))

class BuyMember(RequestHandler):
    def post(self, *args, **kwargs):
        try:
            user_id =int(self.post_argument('user_id'));
            act_id=int(self.post_argument('act_id'));
            df = US.query_by_id(user_id);
            if(df.loc[0,'is_member']==1):
                self.write(Result.fail2(Result.CREATE_MEMBER_FAIL))
                return;
            #充钱。。。。
            succ=True;
            US.buy_vip(user_id,act_id,succ);
            df = US.query_by_id(user_id);
            self.write(Result.succ(df.to_json(orient='records')))
        except Exception as e:
            logger.exception('fail');
            self.write(Result.fail2(Result.ERROR_SYS))

class Suggest(RequestHandler):
    def post(self, *args, **kwargs):
        txt=self.post_argument('txt');
        user_id=self.post_argument('user_id');
        df = US.query_by_id(user_id);
        name=df.loc[0,'name'];
        suggest_log.info('%d,%s,%s'%(user_id,name,txt));