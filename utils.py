#!/usr/bin/env python
# encoding: utf-8
"""
utils.py

Created by jack ju on 2015-03-16.
Copyright (c) 2015 TIKY. All rights reserved.
"""
import threading
import time


class Status(object):
    """
    状态机，封装起来为了保证多线程安全
    """
    INITINAL = 0        # 初始状态
    CHECKING = 1        # Check 密码的阶段
    INSERVICES = 2      # 服务进行中

    def __init__(self):
        self.__locker = threading.Lock()
        self.__value = Status.INITINAL

    def set(self, value):
        self.__locker.acquire()
        try:
            self.__value = value
        finally:
            self.__locker.release()

    @property
    def value(self):
        self.__locker.acquire()
        try:
            value = self.__value
        finally:
            self.__locker.release()

        return value


class Timing(object):
    """
    计时类，用来计算提供服务的时间
    """
    def __init__(self):
        self.__start = None

    def start(self):
        self.__start = time.time()

    def end(self):
        now = time.time()
        return int(self.__start), int(now - self.__start)

if __name__ == '__main__':
    # status = Status()
    # print status.value
    # status.set(Status.CHECKING)
    # print status.value
    # status.set(Status.INSERVICES)
    # print status.value

    timing = Timing()
    timing.start()

    time.sleep(1)

    print timing.end()

    timing.start()

    time.sleep(2)

    print timing.end()

    timing.start()

    time.sleep(3)

    print timing.end()
