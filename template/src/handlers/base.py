#! /usr/bin/env python
# encoding: utf-8

import sys

import tornado.gen
import tornado.web
from tornado.escape import json_encode

from exception import (
    GodError
)
import log


class BaseHandler(tornado.web.RequestHandler):
    """
    BaseHandler
    """
    def __init__(self, *args, **kwargs):
        """
        """
        self.args = None
        super(BaseHandler, self).__init__(*args, **kwargs)

    def send_response(self, body=None, error_code=0, error_msg=None):
        """
        """
        self.clear()
        result = {"code": error_code, "msg": error_msg}

        if body:
            result.update({"data": body})

        self.write(json_encode(result))
        self.finish()

    def preproccess_args(self):
        """
        """
        # return body
        self.args = self.request.body

    def _handle_exception(self, e):
        log_trace = True

        # TODO put exception code to global vars
        if isinstance(e, ValueError):
            reason = "value error:%s" % e
            error_code = -1
        elif isinstance(e, KeyError):
            reason = "key(%s) required." % e
            error_code = -1
        elif isinstance(e, TypeError):
            reason = "type error: %s" % e
            error_code = -1
        elif isinstance(e, tornado.web.MissingArgumentError):
            reason = repr(e)
            error_code = -2
        elif isinstance(e, GodError):
            reason = repr(e)
            error_code = -1
        else:
            reason = "failed:%s" % e
            error_code = -1

        if log_trace:
            log.error(reason, exc_info=sys.exc_info())
        else:
            log.error(reason)

        # 其他函数已经处理过，不再继续
        if self._finished:
            return

        # 因为客户端会把服务端的内容全部打出来，这里暂时隐藏掉
        reason = ""

        self.send_response(
            body=None,
            error_code=error_code,
            error_msg=reason
        )
