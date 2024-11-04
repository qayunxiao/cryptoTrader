# -*- coding: UTF-8 -*-
# @Time    : 2023/3/13 9:43
# @Author  : alvin
# @File    : handle_main.py
# @Software: PyCharm
import os
import sys

from api_list.handle_ahr999new import get_api_ahr999new
from utils.handle_ddmsg import send_ding_msg_byfilepath, send_ding_msgs

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

    dd_msg_info = []
    # print("获取恐慌数据并离线计算")
    resapi_fear = get_api_fear()
    resapi_fear.write_fear_data()
    startDay = '2017-12-17'
    resapi_fear.deal_fear_data_all(skipdays=startDay)
    startDay = '2021-11-10'
    resapi_fear.deal_fear_data_all(skipdays=startDay)
    fear_value = resapi_fear.get_current_fear_value()
    # print("今日恐慌指数:",fear_value)
    # print("获取ahr999指数數據并离线计算")
    res_ahr = get_api_ahr999new()
    resapi_ahr=res_ahr.get_ahr_table()
    # print(resapi_ahr['data'])
    resapi_ahr_data_today ={
        "ahr999":resapi_ahr['data'][0].get("ahr999",0),
        "ahrChange": resapi_ahr['data'][0].get("ahrChange", 0),
        "avg": resapi_ahr['data'][0].get("avg", 0),
        "avgChange": resapi_ahr['data'][0].get("avgChange", 0),
        "value": resapi_ahr['data'][0].get("value", 0),
        "valueChange": resapi_ahr['data'][0].get("valueChange", 0),
        "date": resapi_ahr['data'][0].get("date", 0)
    }
    resapi_ahr_data_yesterday ={
        "ahr999":resapi_ahr['data'][1].get("ahr999",0),
        "ahrChange": resapi_ahr['data'][1].get("ahrChange", 0),
        "avg": resapi_ahr['data'][1].get("avg", 0),
        "avgChange": resapi_ahr['data'][1].get("avgChange", 0),
        "value": resapi_ahr['data'][1].get("value", 0),
        "valueChange": resapi_ahr['data'][1].get("valueChange", 0),
        "date": resapi_ahr['data'][1].get("date", 0)
    }
    import time
    tmp=resapi_ahr_data_today["date"]
    # print("tmp is :{}".format(tmp))
    today_date=time.localtime(tmp/1000)
    date_day=time.strftime("%Y-%m-%d %H:%M:%S", today_date)
    # print("resapi_ahr_data_today is :{}".format(resapi_ahr_data_today["date"]))
    # print("resapi_ahr_data_yesterday is :{}".format(resapi_ahr_data_yesterday["date"]))

    msg_01="恐慌和ahr指标汇总:日期：{},恐慌指数:{} ,昨天恐慌指数:{}, ahr999值:{},昨天ahr999值:{},定投线1.2,""抄底线0.45 ,200日定投成本:{}".format(
        date_day, (fear_value[0]),  fear_value[1],(resapi_ahr_data_today["ahr999"]),(resapi_ahr_data_yesterday["ahr999"]),  (resapi_ahr_data_today['avg']))
    # print(msg_01)
    log.warning(msg_01)
    # print("date_day is :{}".format(date_day))

     # 综合抄底判断
    if fear_value[0] < 40 or resapi_ahr_data_today["ahr999"] < 0.5:
    # if fear_value[0] < 40:
        log.error("Tips综合抄底判断:当前恐慌指数:40,当前ahr999值:0.5 考虑分批抄底，当恐慌低于20是理想抄底机会".format(fear_value[0], resapi_ahr_data_today['ahr999']))
        send_ding_msgs("Tips综合抄底判断:当前恐慌指数:40,当前ahr999值:0.5 考虑分批抄底，当恐慌低于20是理想抄底机会".format(fear_value[0], resapi_ahr_data_today['ahr999']))

    # 逃顶判断
    if fear_value[0] > 90 or resapi_ahr_data_today["ahr999"]  > 1.2:
    # if fear_value[0] > 90:
        log.error("恐慌和ahr指标综合,当前恐慌指数:{},当前ahr999值:{} 考虑分批减仓".format(fear_value[0], resapi_ahr_data_today['ahr999']))
        send_ding_msgs("综合逃顶判断:当前恐慌指数:{},当前ahr999值:{} 考虑分批减仓".format(fear_value[0], resapi_ahr_data_today['ahr999']))

    try:
        symbol_list = ['DOT']
        # symbol_list = ['BTC', 'DOT', 'ETH', 'ICP', 'LINK', 'UNI']
        print("{}:全量币安交易所行情token处理开始.....".format((time.strftime('%Y年%m月%d日'))))
        for token in symbol_list:
            time.sleep(4)  # 控制频率
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
        receicers = ["qawanghailin@gmail.com", "kaysen820@gmail.com"]
        attachmentFile = get_newlogfile()
        # send_mail(receicers, attachmentFile)
        # send_ding_msg_byfilepath(attachmentFile)
        # send_ding_msgs(msg_01)

