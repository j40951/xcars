#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by jack ju on 2015-03-16.
Copyright (c) 2015 TIKY. All rights reserved.
"""

import threading
import time


def hello(name):
    print "hello %s\n" % name

    global timer
    timer = threading.Timer(2.0, hello, ["Hawk"])
    timer.start()

if __name__ == "__main__":
    start = time.time()

    time.sleep(2)

    a = int(time.time() - start)

    print a
    # timer = threading.Timer(2.0, hello, ["Hawk"])
    # timer.start()
    #
    # while True:
    #     time.sleep(1)
    #     print 'hell xxxxxx'