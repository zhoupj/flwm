'''

生成ssl证书http://www.yeolar.com/note/2015/04/30/tornado-ssl-https/
'''

# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import url, RequestHandler
from app.handler.UserHandler import Register,Login,Quit,BuyMember,Suggest,MemberActivity
from app.handler.ErrorHandler import  ErrorHandler;

#https://blog.csdn.net/tichimi3375/article/details/82109679

define('port', default=8793, type=int, help='run server on the given port.')

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r'/user/register', Register),
        (r'/user/login', Login),
        (r'/user/quit', Quit),
        (r'/user/member_activity', MemberActivity),
        (r'/user/buy_member',BuyMember),
        (r'/user/suggest', Suggest)
        #url(r'/python', ItcastHandler, {'subject': 'python'}, name='python_url')
    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


