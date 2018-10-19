# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import url, RequestHandler

define("port", default=8000, type=int, help="run server on the given port.")


class Indexhandler(RequestHandler):
    def get(self):
        python_url = self.reverse_url("python_url")
        print(self.request)
        self.write('<a href="%s">itcast</a>' %
                   python_url)


class ItcastHandler(RequestHandler):
    def initialize(self, subject):
        self.subject = subject

    def get(self):
        self.write(self.subject)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", Indexhandler),
        (r"/cpp", ItcastHandler, {"subject": "c++"}),
        url(r"/python", ItcastHandler, {"subject": "python"}, name="python_url")
    ],
        debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()