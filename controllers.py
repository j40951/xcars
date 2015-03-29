#!/usr/bin/env python
# encoding: utf-8
"""
controllers.py

Created by jack ju on 2015-03-15.
Copyright (c) 2015 TIKY. All rights reserved.
"""
import pyxhook
import logging
import threading
from models import UserModel
from utils import Status
from utils import Timing


class Controller(object):

    INPUT_TIMEOUT = 60
    SERVICE_TIMEOUT = 180

    """
    控制类，Application中的成员变量，监控键盘事件，控制着终端的所有流程
    """
    def __init__(self):
        self.__logger = logging.getLogger()

        # 状态机，0为初始态，1为校验态（输完手机号码），2为服务态
        self.__status = Status()

        self.__user = UserModel()

        # Create hookmanager
        self.__hookmgr = pyxhook.HookManager()

        # Define our callback to fire when a key is pressed down
        self.__hookmgr.KeyDown = self.__keyboard_event

        # Hook the keyboard
        self.__hookmgr.HookKeyboard()

        self.__hookmgr.start()

        # 定时器对象，初始值为None
        self.__timer = None

        # 计时对象
        self.__timing = Timing()

    def __keyboard_event(self, event):
        """
        判断按键，不是数字键0-9，Esc键（Scancode 9），Backspace键（Scancode 22），Enter键就忽略（Scancode 36）
        """
        print event
        if event.ScanCode == 9:   # Esc键，复位
            print "Press Esc"
            self.__timer.cancel()   # 先停定时器
            self.__on_outservices()
        elif 10 <= event.ScanCode <= 19:     # 数字键
            self.__append_number(event)
        if event.ScanCode == 22:    # Backspace
            print "Press Backspace"
            self.__pop_number()
        elif event.ScanCode == 36:  # Enter
            print "Press Enter"
            self.__enter()

    def __reset(self):
        """
        Esc按键调用，reset 成初始状态，终止服务
        """
        self.__status.set(Status.INITINAL)
        self.__user.clean()

    def __enter(self):
        if self.__status.value == Status.INITINAL:
            if UserModel.ZERO < self.__user.len_moobile < UserModel.MAXLEN_MOBILE:
                # self.__timer.cancel()
                print "User not Exist."
                self.__user.clean_mobile()
        elif self.__status.value == Status.CHECKING:
            if UserModel.ZERO < self.__user.len_passwd < UserModel.MAXLEN_PASSWD:
                # self.__timer.cancel()
                print "Password is error."
                self.__user.clean_passwd()
        else:
            pass

    def __append_number(self, event):
        if self.__status.value == Status.INITINAL:
            if self.__user.len_moobile == UserModel.ZERO:
                # 如果是第一次输入数字，则启动定时器
                self.__timer = threading.Timer(Controller.INPUT_TIMEOUT, self.__on_outinput)
                self.__timer.start()

            if self.__user.append_mobile(event.Key) is True and self.__user.len_moobile == UserModel.MAXLEN_MOBILE:

                self.__logger.info("Request get url http://www.bbxiche.com/mobile")
                # 成功，则发送设置状态，失败，则Reset
                self.__status.set(Status.CHECKING)

            print self.__user.str_mobile

        elif self.__status.value == Status.CHECKING:

            if self.__user.append_passwd(event.Key) is True and self.__user.len_passwd == UserModel.MAXLEN_PASSWD:
                self.__logger.info("Request Check passwd, passwd = %s" % self.__user.str_passwd)

                # 密码校验成功，停止Input定时器
                self.__timer.cancel()

                # 校验密码成功，则设置状态为INSERVICES，失败，则重输入密码
                self.__status.set(Status.INSERVICES)
                self.__timing.start()

                # 设置服务超时定时器， 超时时间为30分钟
                self.__timer = threading.Timer(Controller.SERVICE_TIMEOUT, self.__on_outservices)
                self.__timer.start()

            print self.__user.str_passwd
        else:
            pass    # 其他时候的状态忽略掉

    def __pop_number(self):
        if self.__status.value == 0:
            self.__user.pop_mobile()
            print self.__user.str_mobile
        elif self.__status.value == 1:
            self.__user.pop_passwd()
            print self.__user.str_passwd
        else:
            self.__logger.warn("The status is invalid, status=%d" % self.__status.value)

    def __on_outinput(self):
        """
        输入定时器超时处理函数
        """
        self.__logger.info("Input timeout, reset return.")
        self.__reset()

    def __on_outservices(self):
        """
        服务超时处理函数
        """
        if self.__status.value == Status.INSERVICES:
            result = self.__timing.end()
            self.__logger.info("User %s's services finished, costtime = %s(s)", self.__user.str_mobile, str(result))
        self.__reset()