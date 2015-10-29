#!/usr/bin/env python
# encoding: utf-8

import tornado

from .base import BaseHandler


class TestHandler(BaseHandler):

    args = None

    @tornado.gen.coroutine
    def post(self):
        try:
            self.preproccess_args()

            self.send_response({"test": "test"})

        except Exception, e:
            self._handle_exception(e)
