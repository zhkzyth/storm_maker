#!/usr/bin/env python
# encoding: utf-8
from base import BaseHandler


class Better404Handler(BaseHandler):

    def _write_404(self):
        self.send_response(
            None,
            error_code=-1,
            error_msg='The api does not exist.'
        )

    def get(self):
        self._write_404()

    def post(self):
        self._write_404()
