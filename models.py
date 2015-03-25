#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by jack ju on 2015-03-16.
Copyright (c) 2015 TIKY. All rights reserved.
"""
import types
import logging
import threading


class UserModel(object):
    """
    用户模型，单体类，全局保存一份数据
    """
    # 类数据成员，定义手机号的最大长度及密码的最大长度
    ZERO = 0
    MAXLEN_MOBILE = 11
    MAXLEN_PASSWD = 6

    def __init__(self):
        self.__locker = threading.Lock()
        self.__mobile = []
        self.__passwd = []
        self.__logger = logging.getLogger()

    def append_mobile(self, ch):
        """
        输入手机号码，手机号码长度不能大于11，如果累加就返回True，否则返回False
        """
        ret = False
        self.__locker.acquire()
        try:
            if isinstance(ch, types.StringType) and (len(self.__mobile) < UserModel.MAXLEN_MOBILE):
                self.__mobile.append(ch)
                self.__logger.debug("[append_mobile] mobile = %s" % str(self.__mobile))
                ret = True
        finally:
            self.__locker.release()

        return ret

    def append_passwd(self, ch):
        """
        输入密码，密码长度不能超过6，如果累加了久返回True，否则返回False
        """
        ret = False
        self.__locker.acquire()
        try:
            if isinstance(ch, types.StringType) and (len(self.__passwd) < UserModel.MAXLEN_PASSWD):
                self.__passwd.append(ch)
                self.__logger.debug("[append_passwd] passwd = %s" % str(self.__passwd))
                ret = True
        finally:
            self.__locker.release()
        return ret

    def pop_mobile(self):
        self.__locker.acquire()
        try:
            # pop 之前判断下长度
            if len(self.__mobile) > 0:
                self.__mobile.pop()
        finally:
            self.__locker.release()

    def pop_passwd(self):
        self.__locker.acquire()
        try:
            # pop 之前判断下长度
            if len(self.__passwd) > 0:
                self.__passwd.pop()
        finally:
            self.__locker.release()

    def clean_mobile(self):
        self.__locker.acquire()
        try:
            self.__mobile = []
        finally:
            self.__locker.release()

    def clean_passwd(self):
        self.__locker.acquire()
        try:
            self.__passwd = []
        finally:
            self.__locker.release()

    def clean(self):
        self.__locker.acquire()
        try:
            self.__mobile = []
            self.__passwd = []
        finally:
            self.__locker.release()

    @property
    def len_moobile(self):
        self.__locker.acquire()
        try:
            mylen = len(self.__mobile)
        finally:
            self.__locker.release()
        return mylen

    @property
    def len_passwd(self):
        self.__locker.acquire()
        try:
            mylen = len(self.__passwd)
        finally:
            self.__locker.release()
        return mylen

    @property
    def str_mobile(self):
        self.__locker.acquire()
        try:
            mystr = ''.join(self.__mobile)
        finally:
            self.__locker.release()
        return mystr

    @property
    def str_passwd(self):
        self.__locker.acquire()
        try:
            mystr = ''.join(self.__passwd)
        finally:
            self.__locker.release()
        return mystr