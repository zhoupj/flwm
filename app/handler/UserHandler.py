from app.common.util.LogUtil import digest_log, logger, suggest_log;
from tornado.web import url, RequestHandler;
from app.handler.BaseHandler import BaseHandler;
from app.common.Result import Result;
from app.service.UserService import US;
from app.service.MemberService import MS;
from app.common.AppException import AppException;
import pandas as pd;
import tornado;


class Register(BaseHandler):
    def post2(self, *args, **kwargs):
        # print(self.get_body_argument("code"));
        # 暂时用openId，当作code，之后要改造
        code = self.get_argument("code");
        name = self.get_argument("name");

        # 调用微信接口换取openId
        # TODO
        open_id = code;
        US.create(open_id, name);
        return US.query(open_id);



class Login(BaseHandler):
    def post2(self, *args, **kwargs):
        code = self.get_argument('code');
        user = US.query(code);
        if (user):
            US.update_login_days(user['id']);
            return user;
        else:
            raise AppException(Result.ERROR_NOT_LOGIN);

class Quit(BaseHandler):
    def post2(self, *args, **kwargs):
        id = int(self.get_argument('user_id'));
        df = US.query_by_id(id)
        US.update_last_login_time(id);
        return 'succ';


class MemberActivity(BaseHandler):
    def post2(self, *args, **kwargs):
        return MS.query_all();

class BuyMember(BaseHandler):
    def post2(self, *args, **kwargs):
        user_id = int(self.get_argument('user_id'));
        act_id = int(self.get_argument('act_id'));
        df = US.query_by_id(user_id);
        if (df.loc[0, 'is_member'] == 1):
            raise AppException(Result.CREATE_MEMBER_FAIL)
        # 充钱。。。。
        succ = True;
        US.buy_vip(user_id, act_id, succ);
        return US.query_by_id(user_id);



class Suggest(BaseHandler):

    def post2(self, *args, **kwargs):
        txt = self.get_argument('txt');
        user_id = self.get_argument('user_id');
        df = US.query_by_id(user_id);
        name = df.loc[0, 'name'];
        suggest_log.info('%d,%s,%s' % (user_id, name, txt));
