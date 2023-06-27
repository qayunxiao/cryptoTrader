#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:alvin
@file: operationConfig.py
@time: 2019/01/18
"""
import configparser
import os
from utils.operationTestdata import TestData


class OperationConfig( object ):

    def __init__(self):
        self.testdata = TestData()

    def get_sendmail_info(self, contents="mail"):
        tmpdict = {}
        config = configparser.ConfigParser()
        config.read( self.testdata.data_dir( 'config', 'config.ini' ),encoding="utf-8-sig" )
        send_user = config.get( contents, 'SEND_USER' )
        send_from = config.get( contents, 'SEND_FROM' )
        host = config.get( contents, 'SMTP_HOST' )
        login_pwd = config.get( contents, 'MAIL_PASS' )

        tmpdict['send_user'] = send_user
        tmpdict['send_from'] = send_from
        tmpdict['login_pwd'] = login_pwd
        tmpdict['host'] = host
        return tmpdict

    def get_apiinfo(self, contents="url"):
        envdic = {}
        config = configparser.ConfigParser()
        config.read( self.testdata.data_dir( 'config', 'config.ini' ),
                     encoding="utf-8-sig" )
        api_fear = config.get( contents, "API_FEAR" )
        api_arh999 = config.get( contents, "API_ARH999" )

        envdic['api_fear'] = api_fear
        envdic['api_arh999'] = api_arh999
        return envdic

    def get_testenv_mysql(self, contents="mysql"):
        '''contents config file flag'''
        mysqldic = {}
        config = configparser.ConfigParser()
        config.read( self.testdata.data_dir( 'config', 'config.ini' ),
                     encoding="utf-8-sig" )
        mysqlhost = config.get( contents, 'HOST' )
        mysqlport = config.get( contents, "PORT" )
        mysqluser = config.get( contents, "USER" )
        mysqlpasswd = config.get( contents, "PASSWD" )
        mysqldatabases = config.get( contents, "DADABASES" )
        mysqlcharset = config.get( contents, "CHARSET" )
        mysqldic['host'] = mysqlhost
        mysqldic['port'] = mysqlport
        mysqldic['user'] = mysqluser
        mysqldic['password'] = mysqlpasswd
        mysqldic['databases'] = mysqldatabases
        mysqldic['charsetdb'] = mysqlcharset
        return mysqldic


if __name__ == "__main__":
    a = OperationConfig()
    print( type( a.get_sendmail_info() ) )
# print(type(a.get_sendmail_info()))
