
from app.common.util.LogUtil import digest_log, logger, suggest_log;
from tornado.web import url, RequestHandler;
from app.handler.BaseHandler import BaseHandler;
from app.common.Result import Result;
from app.service.UserService import US;
from app.service.MemberService import MS;
from app.common.AppException import AppException;
import pandas as pd;
import tornado;

class SearchHandler(BaseHandler):

    def post2(self, dict):

        user_id=dict['user_id']
        dt=dict['dt'];

        rps250=dict['rps250'];#member
        rps120 = dict['rps120'];#member
        rps50=dict['rps50']#member

        f_hd=dict['fd_hd'];
        s_hd=dict['sb_hd'];#member
        h_hd=dict['hk_hd'];#member
        h_hd_m=float(dict['hk_hd_m']);#member

        n_s2= dict['ns2']#member
        n_s8 = dict['ns8']

        d250=dict['d250'];
        d120=dict['d120'];#meber

        f250=dict['f250'];
        f120=dict['f120'];#member
        f80=dict['f80'];#member

        h50=dict['h50'];
        h0=dict['h']

        hm50=dict['hm50']#c>h(50)
        cmy=dict['cmy'];#(c>yh)

        total=dict['total']
        pe=dict['pe'];
