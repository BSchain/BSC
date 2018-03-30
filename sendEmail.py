# -*- coding: utf-8 -*-
# @Time    : 30/03/2018 11:40 AM
# @Author  : 伊甸一点
# @FileName: sendEmail.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io
# !/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.126.com"  # 设置服务器
mail_user = "bsc_admin@126.com"  # 用户名
mail_pass = "bscadmin2018"  # 口令

sender = 'bsc_admin@126.com'
receivers = ['zpflyfe@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText('网易鼓励企业用户在遵守互联网标准的前提下，向网易邮箱用户发送已经许可的邮件。为了确保您的邮件能及时准确的投递到网易邮箱，请首先确认您没有违背网易的反垃圾政策', 'plain', 'utf-8')
message['From'] = 'bsc_admin@126.com'
message['To'] = 'zpflyfe@163.com'

subject = 'Python SMTP'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print(str(e))
    print("Error: 无法发送邮件")