#!/usr/bin/env python

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options
from settings import settings
from urls import url_patterns

class MakeApp(tornado.web.Application):
  def __init__(self):
    tornado.web.Application.__init__(self, url_patterns, **settings)


def main():
  app = MakeApp()
  http_server = tornado.httpserver.HTTPServer(app)
  http_server.listen(int(os.environ.get("PORT", 5000)))
  # http_server.bind(options.port)
  # http_server.start(0)
  print('connected...')
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()
