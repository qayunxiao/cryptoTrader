# -*- coding: utf-8 -*-
# @Time    : 2019/6/12 21:43
# @Author  : alvin
# @File    : mygreenlet.py
# @Software: PyCharm
# 我自己封装了gevent 的方法,重载了run
from gevent import Greenlet


class MyGreenlet( Greenlet ):
    def __init__(self, func):
        Greenlet.__init__( self )
        self.func = func

    def _run(self):
        # gevent.sleep(self.n)
        self.func
