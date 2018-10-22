from app.common.util.DBPool import dbPool;
import  pandas as pd;
import random;
import datetime

'''
  publish_time datetime not null,
                url varchar(512) not null ,
                title varchar(128) not null,
                digest varchar(256) not null,
                ctx text ,
                visit_count int default 0,
                comment_count int default 0,
                feature text ,'''

TB_NAME='share_article';
class ArticleService:

    def create_spider(self,url):

        df=pd.DataFrame();
        df.loc[0,'url']=url;
        #爬虫
        df.loc[0,'title']='title';

        dbPool.insert(TB_NAME,df);

    def create_all(self,url,title,digest,ctx):
        df = pd.DataFrame();
        df.loc[0, 'url'] = url;
        df.loc[0, 'ctx'] = ctx;
        df.loc[0,'digest']=digest;
        df.loc[0, 'title'] = title;
        df.loc[0,'visit_count']=random.randint(358,9847);
        df.loc[0,'comment_count']=0;
        df.loc[0,'publish_time']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:$S');
        dbPool.insert(TB_NAME, df);

    def query_detail(self,id):
        df= dbPool.query_any('select  id,publish_time,url,title,ctx,visit_count from %s where id=%d'%(TB_NAME,id));
        df.loc[0,'visit_count']=df.loc[0,'visit_count']+1;
        dbPool.update(TB_NAME,df[['id','visit_count']],primaryKeys=['id'])
        return df;


    def query_list(self,pageNo=0,pageSize=5):
        if(pageNo<=0):
            pageNo=0;
        if(pageSize<=0):
            pageSize=5;
        start=pageNo*pageSize;
        return dbPool.query_any('select id,publish_time,url,title,digest,visit_count from %s order by publish_time desc limit %d,%d'%(TB_NAME,start,pageSize));

AS=ArticleService()
if(__name__=='__main__'):
    url='https://finance.sina.com.cn/stock/jsy/2018-10-22/doc-ifxeuwws6920051.shtml';
    title='收评：沪指涨4.09%券商集体涨停 两市成交额达4000亿';
    digest='新浪财经讯 10月22日消息，受到周末各种利好的影响，今日三大股指集体大幅高开，随后在大金融板块的带动下不断冲高，沪指强势收复2600点，创业板指重回1300点，创指最大涨幅达6%，临近收盘两市有所回落。两市超200只个股涨停，全天成交额超4100亿元，上一交易日约为2870亿元。'
    ctx='''
    从盘面来看，各板块悉数大涨，金融股领涨，尤其是券商板块，40只券商股集体涨停；受IPO被否企业重组上市间隔期缩短政策提振，ST板块上演涨停潮；酒店餐饮、白酒、服装家纺等消费股受资金热烈追捧涨幅居前，其次是次新股、军工等板块也有不错的涨幅。今日，康美药业(14.090, -0.48, -3.29%)跌停开盘，随后被巨量资金撬开跌停，盘中最大涨超6%，全天成交金额超72亿，换手率超18%。金发科技(4.040, 0.37, 10.08%)拟斥资超10亿回购股份，一字涨停。
　　截止收盘，沪指报2654.88点，涨幅4.09%，深成指报7748.82点，涨幅4.89%；创指报1314.94点，涨幅5.20%。

　　新浪财经首席评论员老艾[微博]表示， 券商股是行情的风向标，时隔两年多再次集体涨停，是牛市重来的信号吗？两天大涨就认为牛市又来了，那也有点盲目乐观了。而且这两天的大涨主要是管理层救市所致，要想迎来真正持久的牛市，必须要靠A股自己才行。连续两天大涨之后，也要注意分化及回落。(阅读全文)
    ''';
    pd.set_option('display.width', None)  # 解决列之间的省略号
    AS.create_all(url,title,digest,ctx);
    print(AS.query_list(0,3))
    print(AS.query_detail(6))
