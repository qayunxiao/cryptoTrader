# -*- coding: UTF-8 -*-
# @Time    : 2023/3/13 9:43
# @Author  : alvin
# @File    : handle_main.py
# @Software: PyCharm
import os
import sys

from handle_ddmsg import  send_ding_msg_byfilepath

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
import time

from utils.crypto.handle_getKline import get_data
from utils.crypto.handle_Kline import dealdata
from utils.handle_email import send_mail
from utils.handle_log import log
from utils.handle_path import get_newlogfile
from api_list.handle_ahr999 import get_api_ahr999
from api_list.handle_fear import get_api_fear
time.sleep(2)

if __name__ == '__main__':

    dd_msg_info=[]
    # print("获取恐慌数据并离线计算")
    resapi_fear = get_api_fear()
    resapi_fear.write_fear_data()
    startDay = '2017-12-17'
    resapi_fear.deal_fear_data_all(skipdays=startDay)
    startDay = '2021-11-10'
    resapi_fear.deal_fear_data_all(skipdays=startDay)
    fear_value = resapi_fear.get_current_fear_value()
    # print("今日恐慌指数:",fear_value)
    print("获取ahr999指数书籍并离线计算")
    resapi_ahr = get_api_ahr999()
    resapi_ahr.write_ahr_data()
    resapi_ahr.deal_ahr_data()
    resapi_ahr.deal_ahr_data(halve=3)
    resapi_ahr.deal_ahr_data(halve=2)
    ahr_value = resapi_ahr.get_ahr999_data()
    ahr_count = resapi_ahr.get_ahr999_count()

    print("恐慌和ahr指标汇总:今日:{},恐慌指数:{},昨日恐慌指数:{},今日ahr999值:{},昨日ahr999值:{},定投线1.2,"
          "抄底线0.45,今日价格:{},拟合价格:{},200日定投成本:{}".format((time.strftime('%Y年%m月%d日')), (fear_value[0]), (fear_value[1]),
                                                       (ahr_value['ahr999']), (ahr_value['yesterdayahr999']),
                                                       (ahr_value['price']), (ahr_value['niheprice']),
                                                       (ahr_value['200'])))
    log.warning("恐慌和ahr指标汇总:今日:{},恐慌指数:{},昨日恐慌指数:{},今日ahr999值:{},昨日ahr999值:{},定投线1.2,"
                "抄底线0.45,今日价格:{},拟合价格:{},200日定投成本:{}".format((time.strftime('%Y年%m月%d日')), (fear_value[0]),
                                                             (fear_value[1]), (ahr_value['ahr999']),
                                                             (ahr_value['yesterdayahr999']),
                                                             (ahr_value['price']), (ahr_value['niheprice']),
                                                             (ahr_value['200'])))
    msg_01="恐慌和ahr指标汇总:今日:{},恐慌指数:{},昨日恐慌指数:{},今日ahr999值:{},昨日ahr999值:{},定投线1.2,抄底线0.45,今日价格:{},拟合价格:{},200日定投成本:{}".format((time.strftime('%Y年%m月%d日')), (fear_value[0]), (fear_value[1]),
                                                       (ahr_value['ahr999']), (ahr_value['yesterdayahr999']),
                                                       (ahr_value['price']), (ahr_value['niheprice']),
                                                       (ahr_value['200']))
    # 综合抄底判断
    if fear_value[0] < 30 and ahr_value['ahr999'] < 0.5:
        log.error("恐慌和ahr指标综合,当前恐慌指数:{},当前ahr999值:{} 抄底合适".format(fear_value[0], ahr_value['ahr999']))

    try:
        symbol_list=['BTC','ETH']
        # symbol_list = ['BTC', 'ETH', 'DOT', 'LTC', 'FIL']
        print("{}:全量币安交易所行情token处理开始.....".format((time.strftime('%Y年%m月%d日'))))
        for token in symbol_list:
            time.sleep(280)  # 控制频率
            symbol = token + '/USDT'
            print("{}:开始下载K线数据{} ...".format(time.strftime('%Y年%m月%d日'), symbol))
            get_data(symbol)
            print("{}:下载K线数据{}完成".format(time.strftime('%Y年%m月%d日'), symbol))
            print("{}:开始计算离线数据{} ...".format(time.strftime('%Y年%m月%d日'), symbol))
            filename = symbol.split('/')[0] + '.csv'
            # print("get_data filename:",filename)
            dealdatatest = dealdata(filename)
            dealdatatest.testMedian()  # 中位数和成交量加权平均价
            dealdatatest.testPtp()  # 极差 自高价的价差
            dealdatatest.testMaxAndMin()  # 跌幅
            dealdatatest.getvoldata()
            print("{}:计算离线数据{}完成 ...".format(time.strftime('%Y年%m月%d日'), symbol))
        print("{}:全量token处理完成".format((time.strftime('%Y年%m月%d日'))))

    except Exception as e:
        raise e

    finally:
        receicers = ["qawanghailin@gmail.com","kaysen820@gmail.com"]
        attachmentFile = get_newlogfile()
        send_mail(receicers, attachmentFile)
        send_ding_msg_byfilepath(dd_msg_info)