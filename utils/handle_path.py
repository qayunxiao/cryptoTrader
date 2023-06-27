# -*- coding: utf-8 -*-
# @Time    : 2023/2/9 16:10
# @Author  : alvin
# @File    : handle_path.py
# @Software: PyCharm
import os
"""
需求：代码在任意路径都可以获取到项目工程的绝对路径
"""
# print(__file__)#当前文件所在的路径
# print(os.path.dirname(__file__))
# print(os.path.dirname(os.path.dirname(__file__)))
#1- 工程路径
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(project_path)

#2- 配置路径
config_path = os.path.join(project_path,'config','config.ini')
print(config_path)

#3- 数据路径
data_ccxt_path = os.path.join(project_path,'data','ccxt_binance_data')
data_investment_path = os.path.join(project_path,'data','investment')
data_job_path = os.path.join(project_path,'data','job_data')
# print("data_ccxt_path",data_ccxt_path)

#5- log路径
log_path = os.path.join(project_path,r'log')
#print(log_path)

def get_newlogfile():
    lists = os.listdir(log_path)                                    #列出目录的下所有文件和文件夹保存到lists
    # print(list)
    lists.sort(key=lambda fn:os.path.getmtime(log_path + "\\" + fn))#按时间排序
    file_new = os.path.join(log_path,lists[-1])                     #获取最新的文件保存到file_new
    print(file_new)
    return file_new

if __name__ == '__main__':
    test=get_newlogfile()
