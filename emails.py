# -*- coding: utf-8 -*-

import smtplib
import poplib
import email
import time
import datetime
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.mime.text import MIMEText


# 时间格式
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


class emailOperate:
    """
    邮件发送接收类
    """

    # 判断字符集
    def guess_charset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    # 解码器
    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def gather_mail(self, email, password, to_addr):
        """
        读取最新邮件

        参数：
            - email：邮箱地址
            - password：授权密码
        """
        pop3_server = 'pop.'+email.split('@')[-1]
        # 开始连接到服务器
        server = poplib.POP3(pop3_server)
        # server.set_debuglevel(1)
        # 认证:
        server.user(email)
        server.pass_(password)
        resp, mails, octets = server.list()
        # 获取最新一封邮件, 注意索引号从1开始:
        resp, lines, octets = server.retr(len(mails))
        # 解析邮件:
        msg_content = b'\r\n'.join(lines).decode()
        msg = Parser().parsestr(text=msg_content)

        # 获取发件人邮箱地址
        value = msg.get("From", '')
        _, addr = parseaddr(value)
        # 只有指定的邮箱发起控制指令才会执行
        if addr != to_addr:
            print("无效邮件不执行")
            return

        # 获取服务收到邮件时间
        received_time = msg.get("Date")
        received_time = received_time[0:received_time.index("+")]+" GMT"
        # 格式时间
        end = datetime.datetime.strptime(received_time, GMT_FORMAT)
        # 获取当前时间
        start = datetime.datetime.now()
        # print (start,"--",end,"**********************",(start-end).seconds)
        if (start-end).seconds > 60*2:
            print("当前指令已经过期不会被执行 ", start-end)
            return

        # 检查是否有内容
        if (msg.is_multipart()):
            # 获取内容 内容可能包含两部分
            parts = msg.get_payload()
            # 遍历内容
            for _, part in enumerate(parts):
                # 获取内容类型 text/plain and text/html
                content_type = part.get_content_type()
                # 判断是不是纯本部内容
                if content_type == 'text/plain':
                    content = part.get_payload(decode=True)
                    charset = self.guess_charset(part)
                    if charset:
                        # 取出邮件内容
                        content = content.decode(charset)
                        # 去除空格和换行
                        ctext = content.replace("\n", "").strip()
                        return ctext

        # 慎重:将直接从服务器删除邮件:
        # server.dele(len(mails))
        # 关闭连接:
        server.quit()

    def send_email(self, from_addr, password, to_addr, subject, content):
        """
        发送邮件

        参数:
            - from_addr:发送邮件邮箱地址
            - password:发送邮箱邮件密码
            - to_addr:接收邮件邮箱地址
            - subject:主题
            - content:内容
        """
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = u'<%s>' % from_addr
        msg['To'] = u'<%s>' % to_addr
        msg['Subject'] = subject
        # 连接服务
        smtp = smtplib.SMTP_SSL('smtp.163.com', 465)
        # 设置debug等级 0：不打印日志 1：打印日志
        smtp.set_debuglevel(0)
        smtp.ehlo("smtp.163.com")
        # 登录邮箱
        smtp.login(from_addr, password)
        # 发送邮件
        smtp.sendmail(from_addr, [to_addr], msg.as_string())
        # 关闭连接
        smtp.quit()
