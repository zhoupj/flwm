
from app.common.util.LogUtil import digest_log;
from app.handler.BaseHandler import  BaseHandler;
from app.common.Result import Result;
from app.service.ArticleService import AS;


class AtcList(BaseHandler):

    def post2(self, *args, **kwargs):
        pageNo = self.get_argument('pn');
        size = self.get_argument('sz');
        return AS.query_list(int(pageNo),int(size));



class AtcDetail(BaseHandler):

    def post2(self, *args, **kwargs):
        id = self.get_argument('id');
        return AS.query_detail(int(id))


