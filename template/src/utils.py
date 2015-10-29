#!/usr/bin/env python
# encoding: utf-8

import os
import time
import calendar
import hashlib
import random
import base64
import datetime

import tornado
import pytz

from settings import (
    CONNECT_TIMEOUT, REQUEST_TIMEOUT
)


def get_real_file_path(script_path, filename=""):
    path = os.path.join(
        os.path.split(
            os.path.realpath(script_path))[0], filename)
    return path


def change_datetime_to_ts(_date_time, format):
    if not _date_time or not format:
        return
    return calendar.timegm(time.strptime(_date_time, format))


def token_generator():
    return base64.b64encode(
        hashlib.sha256(str(random.getrandbits(256))).digest(),
        random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])
    ).rstrip('==')


def get_utc_time_stamp():

    d = datetime.datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    return unixtime


def prepare_request(
        url=None,
        header=None,
        request_body=None,
        connect_timeout=CONNECT_TIMEOUT,
        request_timeout=REQUEST_TIMEOUT,
        method='POST',
        validate_cert=True
        ):
    # 准备request对象
    request = tornado.httpclient.HTTPRequest(
        url,
        method=method,
        headers=header,
        body=request_body,
        connect_timeout=connect_timeout,
        request_timeout=request_timeout,
        validate_cert=validate_cert)

    return request


def get_local_time_in_iso():

    local_tz = pytz.timezone('Asia/Shanghai')

    return datetime.datetime.now(local_tz).isoformat()
