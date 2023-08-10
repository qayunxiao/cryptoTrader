# -*- coding: utf-8 -*-
# @Time    : 2023/3/22 9:44
# @Author  : alvin
# @File    : handle_email.py
# @Software: PyCharm
"""
 pop.qq.com  995
 smtp.qq.com 465
"""
import os
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from utils.operationConfig import OperationConfig


def send_mail(receicers,attachmentFile,messagetilte="_crypto分析数据"):
    # print(receicers,attachmentFile)
    confdata = OperationConfig().get_sendmail_info()
    # print("confdata",confdata)
    mail_user=confdata['send_user']
    sender=confdata['send_from']
    mail_pass=confdata['login_pwd']
    mail_host=confdata['host']
    #授权码
    # print(mail_host,mail_user,sender,mail_pass)
    #内容
    message = MIMEMultipart()
    #hmtl 文字红色
    message['From']=Header(sender)
    #标题
    Subject=time.strftime("%Y年%m月%d日")+messagetilte
    message['Subject']=Header((Subject),'utf-8')
    #组装附件内容
    filenames= os.path.basename(attachmentFile)
    attr=MIMEText( open(attachmentFile, 'rb' ).read(), 'base64', 'utf-8' )
    attr["Content-Type"]="application/octet-stream"
    attr["Content-Disposition"]='attachment;filename='+filenames
    message.attach(attr)

    #标题
    with open(attachmentFile,'r',encoding='utf-8') as f:
        contents=f.read()
        # print("contents",contents)
    message.attach(MIMEText(contents,'plain','utf-8'))
    try:
        smtpobj = smtplib.SMTP()
        smtpobj.connect(mail_host,25)
        smtpobj.login(mail_user,mail_pass)
        smtpobj.sendmail(sender,receicers,message.as_string())
        # print("email send over!")
    except smtplib.SMTPException as e:
        print("error:{}".format(e))


if __name__ == '__main__':
    receicers=[ "qawanghailin@gmail.com"]
    attachmentFile=r'D:\Sourcetree\yunxiao\cryptoTrader\log\crypto_20230627_1304.log'
    send_mail = send_mail(receicers,attachmentFile)