
from app.common.util.LogUtil import digest_log;
from tornado.web import url, RequestHandler;
from app.common.Result import Result;
from app.service.UserService import UserService;


class Index(RequestHandler):



    def post(self):
        # 暂时用openId，当作code，之后要改造
        code = self.get_argument('code');
        name = self.get_argument('name');
        # 调用微信接口换取openId
        # TODO
        openId = code;

        us=UserService();


        python_url = self.reverse_url("python_url")
        print(self.request)
        self.write('<a href="%s">itcast</a>' %
                   python_url)
