# -*- coding: utf-8 -*-
# -------------------------
# @Time    :  2024/1/2 12:04
# @Author  : alvin
# @Description:  func
# -------------------------
import datetime
import os
import sys
import time


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
utils = os.path.join(BASE_DIR, 'utils')
process_data = os.path.join(BASE_DIR, 'process_data')
sys.path.append(BASE_DIR)
sys.path.append(utils)
sys.path.append(process_data)
# print("utils is :{}".format(utils))
from utils.handle_ddmsg import send_ding_msgs
from utils.crypto.handle_getKline import get_data_Xprice, get_data_price
from process_data.symbol_price_history import get_history_data


class run_priceX():

    def __init__(self):
        self.today_price_list = []
        self.symbol_price = ['BTC', 'ETH', 'DOT', 'LINK', 'FIL', 'OP', 'SOL', 'ENS', 'NEAR', 'PEOPLE', 'SNX',
                             'DYDX', 'STX', 'DASH', 'LDO', 'SAND', 'APE', 'MATIC', 'DOGE', 'ICP', 'APT', 'ADA', 'MAGIC',
                             'MINA', 'MANTA', 'ATOM', 'PYTH', 'BLUR', 'ALT', 'TIA', 'SEI']
        self.costPricedic = {'BTC': 21328, 'ETH': 1588, 'DOT': 7, 'LINK': 6.5, 'FIL': 4.5, 'OP': 3.22, 'SOL': 64,
                             'ENS': 20,
                             'NEAR': 1.1, 'PEOPLE': 0.0285, 'SNX': 3.8, 'DYDX': 1.96,
                             'STX': 0.49, 'DASH': 30, 'LDO': 3.05, 'SAND': 0.7, 'APE': 1.28, 'MATIC': 0.78,
                             'DOGE': 0.0916,
                             'ICP': 3.52, 'APT': 8.7, 'ADA': 0.26, 'MAGIC': 1.24,
                             'MINA': 0.66, 'MANTA': 2.55, 'ATOM': 7.1, 'PYTH': 0.34, 'BLUR': 0.62, 'ALT': 0.35,
                             'TIA': 15,
                             'SEI': 0.59}
        self.symbol_price_history = ['BTC', 'ETH', 'DOT', 'FIL', 'LINK', 'UNI']

    def run_get_history_data(self):
        get_history_data(self.symbol_price_history)

    def run_get_current_price(self):
        get_data_price(self.symbol_price, str(datetime.datetime.now().date()), self.today_price_list)
        send_ding_msgs("日期是:{},中长线持仓成本价:{}".format(str(datetime.datetime.now().date()), self.costPricedic))
        send_ding_msgs("日期是:{},中长线持仓成本价:{}".format(str(datetime.datetime.now().date()), self.costPricedic),myself='alvin')

    def run_get_current_Xprice(self):
        X_List = [2, 3, 4, 5, 6, 7]
        for x in X_List:
            get_data_Xprice(self.symbol_price, self.costPricedic, x, self.today_price_list)
        print("run_get_current_Xprice is end !")


if __name__ == '__main__':
    run_x = run_priceX()
    run_x.run_get_history_data()
    run_x.run_get_current_price()
    run_x.run_get_current_Xprice()
