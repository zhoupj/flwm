
from app.common.util.LogUtil import digest_log;
from app.handler.BaseHandler import  BaseHandler;
from app.common.Result import Result;
from app.service.ArticleService import AS;


class AtcList(BaseHandler):

    def post2(self,dict):
        pageNo = dict['pn'];
        size = dict['sz'];
        return AS.query_list(int(pageNo),int(size));

class AtcDetail(BaseHandler):

    def post2(self, dict):
        id = dict['id'];
        return AS.query_detail(int(id))


