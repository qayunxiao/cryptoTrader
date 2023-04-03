# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 15:38
# @Author  : alvin
# @File    : handle.py
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


class get_api_fear():

    def __init__(self):
        self.confdata = OperationConfig().get_apiinfo()
        self.current_fear_value = []
        self.filepath= os.path.join(data_ccxt_path,"FEAR.csv")
        self.url = self.confdata['api_fear']
        self.headers = {
            "authority":"alternative.me",
            "method":"POST",
            "path":"/api/crypto/fear-and-greed-index/history",
            "scheme":"https",
            "accept":"gzip, deflate, br",
            "accept-encoding":"zh-CN,zh;q=0.9",
            "content-length":"11",
            "content-type": "application/json",
            "cookie":'_ga=GA1.2.1952982792.1679038387; _gid=GA1.2.757896586.1679038387; dancer.session=4bNxNCrAZnWDLXEdntncLC8YtCa3d27ces6M17NEVl8~1710574873~SDKRk0AopDZ7sbAPGs99vA~8AUmranQnHCrBIfHuMJJu94d1Qm-iQGUPhudSptk9tg~2',
            "origin":"https://alternative.me",
            "referer": self.url,
            "sec-ch-ua":"?0",
            "sec-fetch-dest":"empty",
            "sec-fetch-site":" same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        }

    def count_days(self,):
        #历史数据2018年2月1日
        untilYear = 2017
        untilMonth = 12
        untilDay = 10
        firstDay = datetime(untilYear,untilMonth,untilDay)
        # print("firstDay",firstDay)
        strtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        # print("str_endDay",strtime)
        # print(type(strtime))
        end_year = datetime.now().year
        end_month = datetime.now().month
        end_day = datetime.now().day
        endDay = datetime(end_year,end_month,end_day)
        # print("endDay",endDay,type(endDay))
        #rrule.DAILY计算天差，此外还有  星期(WEEKLY)，年（YEARLY）
        days = rrule.rrule(freq = rrule.DAILY,dtstart=firstDay,until=endDay)
        # print('相差:',days.count(),'天')
        count=days.count()
        # self.day_count=days.count()
        return count

    def get_fear(self):
        self.day_count= self.count_days()
        data={"days": self.day_count}
        # print("url:",self.url)
        # print("data",data)
        res = requests.post(url=self.url,json=data)
        data_fear=res.json()['data']['datasets'][0]['data']
        data_date=res.json()['data']['labels']
        # print(type(data_fear),data_fear)
        # print("data_date",data_date)

        return data_fear,data_date

    def write_fear_data(self):
        # print("——————————————write_fear_data————————————————————",self.filepath)
        data_fear,data_date =self.get_fear()
        if os.path.exists(self.filepath):  # 判断文件是否存在
            os.remove(self.filepath)
        with open(self.filepath,"w",newline='',encoding='utf-8') as csv_f:
            fieldnames = ['date', 'fear值','日期']
            writer=csv.DictWriter(csv_f,fieldnames=fieldnames)
            writer.writeheader()#写表头
            # print(data_fear[0],data_fear[1])
            for i in range(len(data_fear)):
                fear = data_fear[i]
                date_d = data_date[i]
                date_d = date_d.split(",")
                # print("date_d[1]",date_d[1])
                # print("date_d[0]",date_d[0])
                date_d= date_d[0] + date_d[1]
                date_d= date_d.replace(' ','-')
                date_d= date_d.replace('Jan','1')
                date_d= date_d.replace('Feb','2')
                date_d= date_d.replace('Mar','3')
                date_d= date_d.replace('Apr','4')
                date_d= date_d.replace('May','5')
                date_d= date_d.replace('Jun','6')
                date_d= date_d.replace('Jul','7')
                date_d= date_d.replace('Aug','8')
                date_d= date_d.replace('Sep','9')
                date_d= date_d.replace('Oct','10')
                date_d= date_d.replace('Nov','11')
                date_d= date_d.replace('Dec','12')
                # print("date_d",date_d) #18-3-2023
                time_array = time.strptime(date_d, '%d-%m-%Y')
                # print("time_array",time_array)
                timestamp = int(time.mktime(time_array))
                # print("timestamp",timestamp)
                dict_tmp={"date":str(timestamp),"fear值":fear,"日期":str(date_d)}
                # print("第{}次".format(i),"---dict_tmp",dict_tmp)
                writer.writerow(dict_tmp)
            # print("write_fear_data is over")

    #获取当日恐慌数据
    def get_current_fear_value(self):
        if (self.current_fear_value !=0):
            # print("current_fear_value",self.current_fear_value)
            return  self.current_fear_value

    def deal_fear_data_all(self,skipdays):
        log.info( "恐慌指数说明:0-24极度恐慌,25-29恐惧,50-74贪婪,75-100极度贪婪，最好策略别人恐慌我贪婪，牛转熊注意，别人贪婪我恐慌")
        if skipdays == '2017-12-17':
            skiprows=1
        else:
            skiprows=1377
            # print("skipdays",skipdays,skiprows)
        fear_list=[]
        dates,fear = np.loadtxt(
            fname=self.filepath,
            delimiter=',',
            skiprows = skiprows, #跳过指定的行
            usecols=(0,1),
            unpack=True,
            encoding='utf-8',
        )
        count_min =0
        count_max =0
        count_total=0
        for i in fear:
            count_total=count_total+1
            fear_list.append(i)
            if i <= 24:
                count_min = count_min +1
            if i >= 75:
                count_max = count_max +1
        if len(self.current_fear_value) == 0 :
            # print("f",self.current_fear_value)
            # print(fear_list[-1],fear_list[-2])
            self.current_fear_value.append(fear_list[-1])
            self.current_fear_value.append(fear_list[-2])
        if (fear_list[-1]) < 24:
            log.warn( "今日恐慌指数:{},请结合AHR999分析是否抄底".format((fear_list[-1]) )    )
            print( "今日恐慌指数:{},请结合AHR999分析是否抄底".format((fear_list[-1]) )    )
        if skipdays == '2017-12-17':
            print( "恐慌指数:从2018年2月1日到今天最高点计算,极度恐慌:{},平均恐慌情绪:{},极度贪婪:{},今日恐慌指数:{}".format(fear.min(),( round(np.average(fear),2)  ),(fear.max()),(fear_list[-1]) )    )
            print( "恐慌指数:从2018年2月1日开始到今天,数据总数:{},其中低于24的极度恐慌次数:{},占比:{}%,其中高于75的极度贪婪次数:{},占比:{}%".format(count_total,count_min,((Decimal((count_min/count_total)).quantize(Decimal('0.00')))*100),count_max,((Decimal((count_max/count_total)).quantize(Decimal('0.00')))*100) ))
            log.info( "恐慌指数:从2018年2月1日到今天最高点计算,极度恐慌:{},平均恐慌情绪:{},极度贪婪:{},今日恐慌指数:{}".format(fear.min(),( round(np.average(fear),2)  ),(fear.max()),(fear_list[-1]) )    )
            log.warn("恐慌指数:从2018年2月1日开始到今天,数据总数:{},其中低于24的极度恐慌次数:{},占比:{}%,其中高于75的极度贪婪次数:{},占比:{}%".format(count_total,count_min,((Decimal((count_min/count_total)).quantize(Decimal('0.00')))*100),count_max,((Decimal((count_max/count_total)).quantize(Decimal('0.00')))*100) ))
        else:
            print( "恐慌指数:从2021年11月10日到今天最高点计算,极度恐慌:{},平均恐慌情绪:{},极度贪婪:{},今日恐慌指数:{}".format(fear.min(),( round(np.average(fear),2)  ),(fear.max()),(fear_list[-1]) )    )
            print( "恐慌指数:从2021年11月10日开始到今天,数据总数:{},其中低于24的极度恐慌次数:{},占比:{}%,其中高于75的极度贪婪次数:{},占比:{}%".format(count_total,count_min,((Decimal((count_min/count_total)).quantize(Decimal('0.00')))*100),count_max,((Decimal((count_max/count_total)).quantize(Decimal('0.00')))*100) ))
            log.info( "恐慌指数:从2021年11月10日到今天最高点计算,极度恐慌:{},平均恐慌情绪:{},极度贪婪:{},今日恐慌指数:{}".format(fear.min(),( round(np.average(fear),2)  ),(fear.max()),(fear_list[-1]) )    )
            log.error( "恐慌指数:从2021年11月10日开始到今天,数据总数:{},其中低于24的极度恐慌次数:{},占比:{}%,其中高于75的极度贪婪次数:{},占比:{}%".format(count_total,count_min,((Decimal((count_min/count_total)).quantize(Decimal('0.00')))*100),count_max,((Decimal((count_max/count_total)).quantize(Decimal('0.00')))*100) ))


if __name__ == '__main__':
    resapi = get_api_fear()
    # resapi.count_days() startDay='2017-12-17'
    resapi.write_fear_data()
    startDay='2017-12-17'
    resapi.deal_fear_data_all(skipdays=startDay)
    startDay='2021-11-10'
    resapi.deal_fear_data_all(skipdays=startDay)
    fear_value=resapi.get_current_fear_value()

