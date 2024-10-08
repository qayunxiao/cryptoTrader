# -*- coding: utf-8 -*-
# -------------------------
# @Time    :  2023/8/8 12:59
# @Author  : alvin
# @Description:  func
# -------------------------
import json
import os
from decimal import Decimal

import numpy as np
from dateutil import rrule
from datetime import datetime

import time
import csv

import requests

from utils.handle_path import data_ccxt_path
from utils.handle_log import log
from utils.operationConfig import OperationConfig


class get_api_ahr999new():
    # https://coinsoto.com/zh/indexdata/ahrIndex
    def __init__(self):
        self.proxies = {
            "http": "http://127.0.0.1:1082"
        }
        self.confdata = OperationConfig().get_apiinfo()
        self.ahr999_count = {}
        self.ahr999_datadict = {}
        self.filepath = os.path.join(data_ccxt_path, "AHR.csv")
        self.url = self.confdata['api_arh999new']
        self.key = self.confdata['api_arh999new_key']
        # print("self.key is :{}".format(self.key))
        self.headers = {
            # "authorization": self.key,
            "authority":"coinsoto.com",
            "method":"GET",
            "path": "/indicatorapi/getAhr999Table",
            "scheme": "https",
            # "accept:": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding":"gzip, deflate, br",
            # "accept-language": "zh-CN,zh;q=0.9",
            "content - type":"application/json",
            "cookie":"i18n_redirected=zh; _ga=GA1.1.913694702.1691644431; kindTips=true; _ga_BDEPVNN1SX=GS1.1.1692844410.3.0.1692844419.0.0.0",
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }

    # 返回get到的data字段
    def get_ahr_table(self):
        # print("url:",self.url)
        res = requests.get(url=self.url, proxies=self.proxies, headers=self.headers)
        if 200 == res.status_code:
            return res.json()


if __name__ == '__main__':
    a = get_api_ahr999new()
    data = a.get_ahr_table()

    print(data['data'])
