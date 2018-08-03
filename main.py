# -*- coding: utf-8 -*-

import emails
import dictate
import config
import time

if __name__ == '__main__':

    # 实例化邮箱类
    email = emails.emailOperate()
    # 实例化系统操作类
    dic = dictate.dictate()
    # 配置文件
    config = config.config()

    while True:
        # 获取邮件内容
        content = email.gather_mail(
            config.from_email, config.password, config.to_addr)
        if content == "关机":
            dic.shutdown()
            email.send_email(config.from_email, config.password,
                            config.to_addr, "远程操控", "计算机正在执行关机指令")
        if content == "重启":
            dic.restart
            email.send_email(config.from_email, config.password,
                            config.to_addr, "远程操控", "计算机正在执行重启指令")
        if content == "取消":
            dic.cancel()
            email.send_email(config.from_email, config.password,
                            config.to_addr, "远程操控", "计算机正在执行取消指令")
        time.sleep(1*60)
