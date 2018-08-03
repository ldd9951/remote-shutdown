# -*- coding: utf-8 -*-

import configparser
import os

class config(object):

    def __init__(self):

        # 项目路径
        rootDir = os.path.split(os.path.realpath(__file__))[0]
        # config.ini文件路径
        configFilePath = os.path.join(rootDir, 'config.ini')

        config = configparser.ConfigParser()
        # 读取配置文件
        config.read(configFilePath)

        # 获取from_email 参数
        self.from_email = config.get("email", "from_email")
        self.password = config.get("email", "password")
        self.to_addr = config.get("email", "to_addr")
        # self.subject = config.get("email", "subject")

        pass
