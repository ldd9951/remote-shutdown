# -*- coding: utf-8 -*-
import platform
import os

# 获取操作系统类型
systemType = platform.system()


class dictate(object):
    """
    用于操作计算机系统
    """

    def shutdown(self):
        """
        执行关闭系统
        """
        pass
        # 判断操作系统
        if systemType == "Windows":
            # 1分钟后关机 单位秒
            os.system("shutdown -s -t 60")
        elif systemType == "Linux":
            # 1分钟后关机 单位分钟
            os.system("shutdown -h 1")

    def restart(self):
        """
        执行重启系统
        """
        # 判断操作系统
        if systemType == "Windows":
            # 执行重启
            os.system("shutdown -r")
        elif systemType == "Linux":
            # 执行重启
            os.system("shutdown -r now")

    def cancel(self):
        """
        取消执行系统指令
        """
        # 判断操作系统
        if systemType == "Windows":
            # 执行取消指令
            os.system("shutdown -a")
        elif systemType == "Linux":
            # 执行重启
            os.system("shutdown -c")
