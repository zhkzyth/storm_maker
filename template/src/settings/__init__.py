#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function


try:
    from .conf.current import *
except ImportError:
    from .conf.dev import *
