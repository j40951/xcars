#!/usr/bin/env python
# encoding: utf-8
"""
main.py

Created by jack ju on 2015-03-15.
Copyright (c) 2015 TIKY. All rights reserved.
"""

import time
import logging.config
import logging
import singleton
import controllers


class Application(singleton.Singleton):
    """
    应用类，单体类
    """
    def __init__(self):
        """
        初始化Application中的成员变量
        """
        self.__running = True

        # 初始化日志组件
        logging.config.fileConfig("etc/conf/logging.properties")
        self.__logger = logging.getLogger()

        # 定义控制类对象
        self.__controller = controllers.Controller()

    def run(self):
        while self.__running:
            time.sleep(0.1)


if __name__ == '__main__':
    theapp = Application()
    theapp.run()
