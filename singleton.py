#!/usr/bin/env python
# encoding: utf-8
"""
singleton.py

Created by jack ju on 2015-03-15.
Copyright (c) 2015 TIKY. All rights reserved.
"""
import threading


class Singleton(object):

    __objs = {}
    __objs_locker = threading.Lock()

    def __new__(cls, *args, **kv):
        if cls in cls.__objs:
            return cls.__objs[cls]['obj']

        cls.__objs_locker.acquire()
        try:
            if cls in cls.__objs:  # double check locking
                return cls.__objs[cls]['obj']
            obj = object.__new__(cls)
            cls.__objs[cls] = {'obj': obj, 'init': False}
            setattr(cls, '__init__', cls.decorate_init(cls.__init__))
        finally:
            cls.__objs_locker.release()
        return obj

    @classmethod
    def decorate_init(cls, fn):
        def init_wrap(*args):
            if not cls.__objs[cls]['init']:
                fn(*args)
                cls.__objs[cls]['init'] = True
            return

        return init_wrap