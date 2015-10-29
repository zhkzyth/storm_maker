#! /usr/bin/env python
# encoding: utf-8
"""
log模块，这里利用了一些sys.modules和python系统库查找的一些trick。

log模块第一次导入的时候，是作为一个文件被查找到的。
查找成功后，文件会跑一个生成log实例的逻辑，然后把它加入到全局sys.modules字典里面。

以后所有模块的`import log`动作都会绕开文件查找的过程，直接在sys.modules里面找这个模块。
"""
import sys
import logging.handlers
from settings import (
    LOG_NAME
)


class Log(object):
    FMT = (
        '[%(levelname)s][%(name)s:%(process)d][%(asctime)s]' +
        ': %(message)s')

    def __init__(self, name):
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        fmt = logging.Formatter(self.FMT)
        ch.setFormatter(fmt)

        log = logging.getLogger(name)
        log.addHandler(ch)

        self.log = log

    def __call__(self):
        return self.log


sys.modules[__name__] = Log(LOG_NAME)()
