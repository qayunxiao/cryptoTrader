#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:alvin
@file: sendmail.py
@time: 2019/01/18
"""
import email, os
import mimetypes
import smtplib
from email.encoders import encode_base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
from utils.operationConfig import OperationConfig


class Mail( object ):
    def __init__(self):
        self.mailinfo = OperationConfig()

    def send_mail_SMTPSSL(self, to_user='', sub='', content=''):
        # '''
        # 发送邮件内容
        # :param to_user:发送邮件的人
        # :param sub:主题
        # :param content:邮件内容
        # '''
        # 邮箱smtp服务器
        host_server = self.mailinfo.get_sendmail_info().get( 'host' )
        sender_sina_mail = self.mailinfo.get_sendmail_info().get( 'from_addr' )
        user = self.mailinfo.get_sendmail_info().get( 'login_user' )
        passwd = self.mailinfo.get_sendmail_info().get( 'login_pwd' )

        # ssl登录
        smtp = SMTP_SSL( host_server )
        # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        smtp.set_debuglevel( 1 )
        smtp.ehlo( host_server )
        smtp.login( user, passwd )
        msg = MIMEText( content, "plain", 'utf-8' )
        msg["Subject"] = Header( sub, 'utf-8' )
        msg["From"] = sender_sina_mail
        # msg["To"] = to_user
        # msg['To'] = ','.join(to_user)  # 邮件上显示的收件人
        smtp.sendmail( sender_sina_mail, to_user, msg.as_string() )
        smtp.quit()

    def send_mail_SMTP(self, to_user, sub='', content=''):
        # '''
        # 发送邮件内容
        # :param to_user:发送邮件的人
        # :param sub:主题
        # :param content:邮件内容
        # '''

        # 发件人
        sender = self.mailinfo.get_sendmail_info().get( 'from_addr' )
        # 所使用的用来发送邮件的SMTP服务器
        smtpServer = self.mailinfo.get_sendmail_info().get( 'host' )
        # 发送邮箱的用户名和授权码（不是登录邮箱的密码）
        username = self.mailinfo.get_sendmail_info().get( 'login_user' )
        password = self.mailinfo.get_sendmail_info().get( 'login_pwd' )
        # 创建一个实例
        message = MIMEText( content, 'plain', 'utf-8' )  # 邮件正文
        message['From'] = sender  # 邮件上显示的发件人
        message['To'] = ','.join( to_user )  # 邮件上显示的收件人
        message['Subject'] = Header( sub, 'utf-8' )  # 邮件主题

        try:
            smtp = smtplib.SMTP()  # 创建一个连接
            smtp.set_debuglevel( 0 )  # 1调试   0不打印调试
            smtp.connect( smtpServer )  # 连接发送邮件的服务器
            smtp.login( username, password )  # 登录服务器
            smtp.sendmail( sender, message['To'].split( ',' ),
                           message.as_string() )  # 填入邮件的相关信息并发送
            print( "邮件发送成功！！！" )
            smtp.quit()
        except smtplib.SMTPException:
            print( "邮件发送失败" )

    def send_mail_SMTP_contentFile(self, to_user, sub='', contentfile=''):
        # '''
        # 发送邮件内容
        # :param to_user:发送邮件的人
        # :param sub:主题
        # :param contentfile:文件路径作为内容
        # '''
        # 发件人
        sender = self.mailinfo.get_sendmail_info().get( 'from_addr' )
        # 所使用的用来发送邮件的SMTP服务器
        smtpServer = self.mailinfo.get_sendmail_info().get( 'host' )
        # 发送邮箱的用户名和授权码（不是登录邮箱的密码）
        username = self.mailinfo.get_sendmail_info().get( 'login_user' )
        password = self.mailinfo.get_sendmail_info().get( 'login_pwd' )
        f = open(contentfile, 'r', errors='ignore')
        if f:
            content=f.read()
        else:
            content="error info file is null"
        # print("content",content)
        # 创建一个实例
        message = MIMEText( content, 'plain', 'utf-8' )  # 邮件正文
        message['From'] = sender  # 邮件上显示的发件人
        message['To'] = ','.join( to_user )  # 邮件上显示的收件人
        message['Subject'] = Header( sub, 'utf-8' )  # 邮件主题

        try:
            smtp = smtplib.SMTP()  # 创建一个连接
            smtp.set_debuglevel( 0 )  # 1调试   0不打印调试
            smtp.connect( smtpServer )  # 连接发送邮件的服务器
            smtp.login( username, password )  # 登录服务器
            smtp.sendmail( sender, message['To'].split( ',' ),
                           message.as_string() )  # 填入邮件的相关信息并发送
            print( "邮件发送成功！！！" )
            smtp.quit()
        except smtplib.SMTPException:
            print( "邮件发送失败" )

    def send_mail_SMTP_attachmentFile(self, to_user, sub='', content='',
                                      *attachmentFilePaths):
        # '''
        # 发送邮件内容
        # :param to_user:发送邮件的人
        # :param sub:主题
        # :param content:邮件内容
        # '''
        # 发件人
        sender = self.mailinfo.get_sendmail_info().get( 'from_addr' )
        # 所使用的用来发送邮件的SMTP服务器
        smtpServer = self.mailinfo.get_sendmail_info().get( 'host' )
        # 发送邮箱的用户名和授权码（不是登录邮箱的密码）
        username = self.mailinfo.get_sendmail_info().get( 'login_user' )
        password = self.mailinfo.get_sendmail_info().get( 'login_pwd' )
        # 创建一个实例
        message = MIMEMultipart( content, 'plain', 'utf-8' )  # 邮件正文
        gmailUser = sender
        gmailPassword = password
        recipient = '6449694@qq.com'

        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = recipient
        msg['Subject'] = sub
        msg.attach( MIMEText( content ) )
        print( "attachmentFilePaths", attachmentFilePaths )
        for attachmentFilePath in attachmentFilePaths:
            print("attachmentFilePath",attachmentFilePath)
            msg.attach( Mail().getAttachment( attachmentFilePath ) )

        mailServer = smtplib.SMTP( smtpServer, 587 )
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login( gmailUser, gmailPassword )
        mailServer.sendmail( gmailUser, recipient, msg.as_string() )
        mailServer.close()

        print( 'Sent email to %s' % recipient )

    def getAttachment(self,attachmentFilePath):
        contentType, encoding = mimetypes.guess_type( attachmentFilePath )

        if contentType is None or encoding is not None:
            contentType = 'application/octet-stream'

        mainType, subType = contentType.split( '/', 1 )
        file = open( attachmentFilePath, 'r' )
        print( "mainType", mainType,file.read() )
        if mainType == 'text':
            attachment = MIMEText( file.read() )
        elif mainType == 'message':
            attachment = email.message_from_file( file )
        elif mainType == 'image':
            attachment = MIMEImage( file.read(), _subType=subType )
        elif mainType == 'audio':
            attachment = MIMEAudio( file.read(), _subType=subType )
        else:
            attachment = MIMEBase( mainType, subType )
        attachment.set_payload( file.read() )
        encode_base64( attachment )

        file.close()

        attachment.add_header( 'Content-Disposition', 'attachment',
                               filename=os.path.basename(
                                   attachmentFilePath ) )
        print("attachment",attachment)
        return attachment


if __name__ == "__main__":
    m = Mail()
    # m.send_mail_SMTPSSL("6449694@qq.com","digitalserver",'digitalserver QATEST')
    to_user = ["6449694@qq.com", "qawanghailin@gmail.com"]
    #
    # m.send_mail_SMTP( to_user, "digitalserver", "AAAAA",
    #                              r'D:\workplace\pycharm2021\AirDrop\data\tokeninfo\LDC.txt' )
    m.send_mail_SMTP_contentFile( to_user, "digitalserver",
                                     r'D:\workplace\pycharm2021\AirDrop\data\tokeninfo\LDC.txt' )
