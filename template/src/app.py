#! /usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornadoredis
import torndb
from tornado.options import options, define

import log
import handlers.test

from settings import (
    DEBUG, PORT, HOST,
    MYSQL_CONFIG, REDIS_CONFIG
)


class Application(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        _handlers = [
            (r"/test/hello", handlers.test.TestHandler),
            (r".*", handlers.common.Better404Handler),
        ]
        _settings = {
            "debug": options.debug,
        }
        self.db = torndb.Connection(**MYSQL_CONFIG)
        self.redis_conn = tornadoredis.Client(**REDIS_CONFIG)

        tornado.web.Application.__init__(self, _handlers, **_settings)


def sig_handler(sig, frame):
    log.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().stop()


def main():
    # Tricks enable some log features of tornado
    options.parse_command_line()

    log.info("server start")

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    app = Application()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port, options.host)

    tornado.ioloop.IOLoop.instance().start()


define("port", default=PORT, help="port", type=int)
define("host", default=HOST, help="host", type=str)
define("debug", default=DEBUG, help="debug mode", type=bool)


if __name__ == '__main__':
    main()
