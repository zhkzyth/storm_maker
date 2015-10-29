#! /usr/bin/env python
# encoding: utf-8


class TimeOutError(Exception):
    pass


class MaxRetryError(Exception):
    pass


class GodError(Exception):
    """
    custom exception msg class
    """
    def __init__(self, msg="Intern Error", code=500):
        self.msg = msg
        self.code = code

    def __str__(self):
        return self.msg
