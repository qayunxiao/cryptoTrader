# -*- coding: utf-8 -*-
# @Time    : 2023/3/18 16:40
# @Author  : alvin
# @File    : handle_ahr999.py
# @Software: PyCharm
import os
from decimal import Decimal

import numpy as np
from dateutil import rrule
from datetime import datetime

import time
import csv

import  requests

from utils.handle_path import data_ccxt_path
from utils.handle_log import log
from utils.operationConfig import OperationConfig


class get_api_ahr999():

    def __init__(self):
        self.confdata = OperationConfig().get_apiinfo()
        self.ahr999_count={}
        self.ahr999_datadict={}
        self.filepath= os.path.join(data_ccxt_path,"AHR.csv")
        self.url = self.confdata['api_arh999']
        self.headers = {
            "authority":"dncapi.soulbab.com",
            "method":"GET",
            "path":"/api/v2/index/arh999?code=bitcoin&webp=1",
            "scheme":"https",
            "accept":'application/json, text/plain, */*',
            "accept-encoding":"gzip, deflate, br",
            "accept-language":"zh-CN,zh;q=0.9",
            "origin":"https://www.feixiaohaozh.info",
            "referer":"https://www.feixiaohaozh.info/",
            "sec-ch-ua":'"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            "sec-ch-ua-mobile":"?0",
            "sec-fetch-dest":"empty",
            "sec-fetch-mode":"cors",
            "sec-fetch-site":"cross-site",
            "user-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        }

    def get_ahr(self):
        # print("url:",self.url)
        res = requests.get(url=self.url)
        data_ahr=res.json()['data']
        # print(data_ahr)
        return data_ahr

    def write_ahr_data(self):
        # print("——————————————write_fear_data————————————————————",self.filepath)
        data_ahr =self.get_ahr()
        if os.path.exists(self.filepath):  # 判断文件是否存在
            os.remove(self.filepath)
        with open(self.filepath,"w",newline='',encoding='utf-8') as csv_f:
            fieldnames = ['date','ahr999','价格','拟合价格','200日定投成本','日期']
            writer=csv.DictWriter(csv_f,fieldnames=fieldnames)
            writer.writeheader()#写表头
            #[1367174841.0, 2.9238, 135.3, 46.274, 135.3]
            for i in data_ahr:
                timestamp = str(i[0]).split(".")
                time_local = time.localtime(float(timestamp[0]))
                # print("timestamp",timestamp[0])
                # 转换成新的时间格式(精确到秒)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                dict_tmp={"date":i[0],"ahr999":i[1],"价格":i[2],"拟合价格":i[3],"200日定投成本":i[4],"日期":dt}
                # print(i[0],i[1],i[2],i[3],i[4],dt)
                writer.writerow(dict_tmp)

    def get_ahr999_data(self):
        if self.ahr999_datadict is not None:
            # print("get_ahr999_data",self.ahr999_datadict)
            return self.ahr999_datadict

# {'抄底': 318, '危险': 1003, '定投': 1111, '总次数': 2432} (round((self.ahr999_count['抄底'])/(self.ahr999_count['总次数']),4))*100)
    def get_ahr999_count(self):
        if len(self.ahr999_count) > 0:
            # print("get_ahr999_count",self.ahr999_count)
            cdp=round((self.ahr999_count['抄底'])/(self.ahr999_count['总次数']),4)
            dtp=round((self.ahr999_count['定投'])/(self.ahr999_count['总次数']),4)
            print( "ahr指标:样本数据总数:{},其中低于0.45的抄底次数:{},占比:{}%,其中适合定投的次数:{},占比:{}%"
                       .format((self.ahr999_count['总次数']),(self.ahr999_count['抄底']),(cdp*100),(self.ahr999_count['定投']),(dtp*100) ))
            log.warn( "ahr指标:样本数据总数:{},其中低于0.45的抄底次数:{},占比:{}%,其中适合定投的次数:{},占比:{}%"
                   .format((self.ahr999_count['总次数']),(self.ahr999_count['抄底']),(cdp*100),(self.ahr999_count['定投']),(dtp*100) ))
            return self.ahr999_count

    def deal_ahr_data(self,halve=None):
        global skiprows
        if halve == 3:
            skiprows=2546
        elif halve == 2:
            skiprows=1152
        else:
            skiprows=2728

        ahr999_list=[]
        date_list=[]
        price_list=[]
        niheprice_list=[]
        day200_list=[]
        date,ahr999,price,niheprice,day200 = np.loadtxt(
            fname=self.filepath,
            delimiter=',',
            skiprows = skiprows, #跳过指定的行
            usecols=(0,1,2,3,4),
            unpack=True,
            encoding='utf-8',
        )
        #把数据加列表
        for i in ahr999:
            ahr999_list.append(i)
        for i in price:
            price_list.append(i)
        for i in niheprice:
            niheprice_list.append(i)
        for i in day200:
            day200_list.append(i)

        # 统计ahr999数据 在0.45和1.2区间内或许适合定投BTC ahr999_count
        count_min =0
        count_max =0
        count_dt = 0
        count_total=0
        for i in ahr999_list:
            count_total=count_total+1
            if i <= 0.45:
                count_min = count_min +1
            elif i >= 1.2:
                count_max = count_max +1
            else:
                count_dt = count_dt+1
        if  count_max != 0 and count_min != 0 and  count_dt !=0 and count_total != 0:
            self.ahr999_count['抄底']=count_min
            self.ahr999_count['危险']=count_max
            self.ahr999_count['定投']=count_dt
            self.ahr999_count['总次数']=count_total

        # 获取当日最新数据
        if (len(self.ahr999_datadict) == 0):
            self.ahr999_datadict['ahr999']=ahr999_list[-1]
            self.ahr999_datadict['price']=price_list[-1]
            self.ahr999_datadict['niheprice']=niheprice_list[-1]
            self.ahr999_datadict['200']=day200_list[-1]
            self.ahr999_datadict['yesterdayahr999']=ahr999_list[-2]
            # print("ahr999_datadict",self.ahr999_datadict)
        #判断减产次数
        if halve == 3:
            print("ahr指标:从2020年5月12日第3次减产开始计算,最低ahr值:{},平均ahr值:{},最高ahr值:{},今日ahr值:{}".format(ahr999.min(),( round(np.average(ahr999),2)  ),(ahr999.max()),(ahr999_list[-1]) ) )
            log.info("ahr指标:从2020年5月12日第3次减产开始计算,最低ahr值:{},平均ahr值:{},最高ahr值:{},今日ahr值:{}".format(ahr999.min(),( round(np.average(ahr999),2)  ),(ahr999.max()),(ahr999_list[-1]) ) )
        elif halve == 2:
            print("ahr指标:从2016年7月9日第2次减产开始计算,最低ahr值:{},平均ahr值:{},最高ahr值:{},今日ahr值:{}".format(ahr999.min(),( round(np.average(ahr999),2)  ),(ahr999.max()),(ahr999_list[-1]) ) )
            log.info("ahr指标:从2016年7月9日第2次减产开始计算,最低ahr值:{},平均ahr值:{},最高ahr值:{},今日ahr值:{}".format(ahr999.min(),( round(np.average(ahr999),2)  ),(ahr999.max()),(ahr999_list[-1]) ) )
        else:
            print("ahr指标说明:当ahr指标低于0.45时或许适合抄底，在0.45和1.2区间内或许适合定投BTC，高于该区间说明此时或许不是良好的定投时机。")
            log.info("ahr指标说明:当ahr指标低于0.45时或许适合抄底，在0.45和1.2区间内或许适合定投BTC，高于该区间说明此时或许不是良好的定投时机。")
            print("ahr指标:从2021年11月10日价格最高开始计算,最低ahr值:{},平均ahr值:{},最高ahr值:{},今日ahr值:{}".format(ahr999.min(),( round(np.average(ahr999),2)  ),(ahr999.max()),(ahr999_list[-1]) ) )
            log.info("ahr指标:从2020年11月10日价格最高开始计算,最低ahr值:{},平均ahr值:{},最高ahr值:{},今日ahr值:{}".format(ahr999.min(),( round(np.average(ahr999),2)  ),(ahr999.max()),(ahr999_list[-1]) ) )
            if (ahr999_list[-1]) < 0.5:
                log.warn("ahr指标:今日:{},当前ahr999值:{},结合恐慌指数考虑是否分批抄底?".format((datetime.today().date()),(ahr999_list[-1])))
            elif (ahr999_list[-1]) > 1.2:
                log.warn("ahr指标:今日:{},当前ahr999值:{},结合恐慌指数考虑是否分批减仓?".format((datetime.today().date()),(ahr999_list[-1])))
            else:
                log.warn("ahr指标:今日:{},当前ahr999值:{},结合恐慌指数考虑是否定投?".format((datetime.today().date()),(ahr999_list[-1])))


if __name__ == '__main__':
    resapi = get_api_ahr999()
    # resapi.get_ahr()
    resapi.write_ahr_data()
    resapi.deal_ahr_data()
    resapi.deal_ahr_data(halve=3)
    resapi.deal_ahr_data(halve=2)
    resapi.get_ahr999_data()
    a=resapi.get_ahr999_count()
