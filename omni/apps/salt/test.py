# -*- coding:utf8 -*-
"""
Created on 15-11-21 下午1:52
@author: FMC

"""
from __future__ import nested_scopes, generators, division, with_statement, print_function

from celery import Celery
import os
import time

app = Celery('test', backend='redis://127.0.0.1:6379/0', broker='redis://127.0.0.1:6379/0')

@app.task(serializer='json')
def ifconfig():
    return os.system('curl http://baidu.com/')


if __name__ == '__main__':
    t = ifconfig.delay()
    print(type(t))
    print(t.state)
    time.sleep(1)
    print(t.state)
    time.sleep(1)
    print(t.state)
    print(t.get())