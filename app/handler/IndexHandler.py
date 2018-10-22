
from app.common.util.LogUtil import digest_log;
from app.handler.BaseHandler import  BaseHandler;
from app.common.Result import Result;
from app.service.ArticleService import AS;


class AtcList(BaseHandler):


    def post2(self, *args, **kwargs):
        pageNo = self.get_argument('pn');
        size = self.get_argument('sz');
        df=AS.query_list(int(pageNo),int(size));
        self.write(Result.succ_df(df))


class AtcDetail(BaseHandler):

    def post2(self, *args, **kwargs):
        id = self.get_argument('id');
        df=AS.query_detail(int(id))
        self.write(Result.succ_df(df))

