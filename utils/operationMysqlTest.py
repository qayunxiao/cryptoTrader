# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 9:42
# @Author  : alvin
# @File    : qatestdb.py
# @Software: PyCharm
import  time
from utils.operationMysql import MySQLAction
from utils.logger import Logger


def qatestinsertsql():

    paramslist=[]
    log=Logger()
    for package_name in range(99, 103):
        sql = "insert into bc_uv_detail (c_date, app_name, company, channel_code, uv_num, create_time, package_name) " \
                  "values (%s, %s, %s, %s, %s, %s, %s )"
        package_name_values = "com.wandoujia.phoenixAa" + str(package_name)
        qudao = "phoenixAa" + str(package_name)
        paramsinfo = (
            1554048000,'腾讯动漫','上海米节信息科技有限公司',
            qudao,package_name,1554083419,package_name_values
        )
        paramslist.append(paramsinfo)
        log.logger.info(paramslist)
        a=MySQLAction()
        res=a.exec_insert(sql,paramslist)


def delsql():
    sqldel = "delete  from  bc_uv_detail WHERE channel_code= 'qudao' and uv_num= 1 "
    data = ('qudao', 1)
    log = Logger()
    log.logger.info(sqldel)
    a = MySQLAction()
    res=a.exec_del(sqldel)
    print(res)

if __name__ == "__main__":
    sql="UPDATE  bc_uv_detail set  channel_code= 'qudao' , uv_num= 1  WHERE channel_code= 'phoenixAa100' and uv_num= 100"
    a = MySQLAction()
    sss="SELECT * from  bc_uv_detail WHERE channel_code= 'phoenixAa99' and uv_num=99 "
    resset =a.exec_search(sss)
    # print(resset)
    for  res in resset:
        id=res[0]
        c_date=res[1]
        app_name=res[2]
        channel=res[3]
        uv=res[4]
        c1time=res[5]
        package=res[6]
        print ("id=%s,c_date=%s,app_name=%s,channel=%s,uv=%s,c1time=%s,package=%s" %(id, c_date, app_name, channel, uv,c1time,package))
    # print(a.exec_del(sql))
    # print(qatestinsertsql())
    # upsql="UPDATE  bc_uv_detail set   channel_code= 'phoenixAa100' , uv_num= 100  WHERE channel_code= 'qudao' and  uv_num= 1"
    # print(a.exec_updata(upsql))