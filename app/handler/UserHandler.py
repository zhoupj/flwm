from app.common.util.LogUtil import digest_log, logger, suggest_log;
from tornado.web import url, RequestHandler;
from app.handler.BaseHandler import BaseHandler;
from app.common.Result import Result;
from app.service.UserService import US;
from app.service.MemberService import MS;
import pandas as pd;


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
        df = US.query(open_id);
        self.write(Result.succ_df(df))


class Login(BaseHandler):
    def post2(self, *args, **kwargs):

        code = self.get_argument('code');
        df = US.query(code);
        if (df.empty):
            self.write(Result.fail2(Result.ERROR_NOT_LOGIN))
        else:
            US.update_login_days(df.loc[0, 'id']);
            self.write(Result.succ_df(df))


class Quit(BaseHandler):
    def post2(self, *args, **kwargs):
        id = int(self.get_argument('user_id'));
        df = US.query_by_id(id)
        US.update_last_login_time(id);
        self.write(Result.succ('udpate sucess'));


class MemberActivity(BaseHandler):
    def post2(self, *args, **kwargs):
        df = MS.query_all();
        self.write(Result.succ(df.to_json(orient='records')));


class BuyMember(BaseHandler):
    def post2(self, *args, **kwargs):
        user_id = int(self.get_argument('user_id'));
        act_id = int(self.get_argument('act_id'));
        df = US.query_by_id(user_id);
        if (df.loc[0, 'is_member'] == 1):
            self.write(Result.fail2(Result.CREATE_MEMBER_FAIL))
            return;
        # 充钱。。。。
        succ = True;
        US.buy_vip(user_id, act_id, succ);
        df = US.query_by_id(user_id);
        self.write(Result.succ(df.to_json(orient='records')))


class Suggest(BaseHandler):
    def post2(self, *args, **kwargs):
        txt = self.get_argument('txt');
        user_id = self.get_argument('user_id');
        df = US.query_by_id(user_id);
        name = df.loc[0, 'name'];
        suggest_log.info('%d,%s,%s' % (user_id, name, txt));
