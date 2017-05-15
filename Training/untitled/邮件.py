#!/usr/bin/env python3
# coding: utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

sender = 'xinxihuoqudeta@163.com'
receiver = '1282412855@qq.com'
subject = 'python email test'
smtpserver = 'smtp.163.com'
username = 'xinxihuoqudeta@163.com'
password = 'xxhqdt'

msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'test message'

# 构造附件
att = MIMEText(open('/Users/guoyinjinrong1/Desktop/ww.png', 'rb').read(), 'base64', 'utf-8')
att["Content-Type"] = 'application/octet-stream'
att["Content-Disposition"] = 'attachment; filename="ww.png"'
msgRoot.attach(att)

smtp = smtplib.SMTP()
smtp.connect('smtp.163.com')
smtp.login(username, password)
smtp.sendmail(sender, receiver, msgRoot.as_string())
smtp.quit()