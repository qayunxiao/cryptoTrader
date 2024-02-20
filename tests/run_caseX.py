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

from handle_ddmsg import send_ding_msgs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
utils = os.path.join(BASE_DIR, 'utils')
sys.path.append(BASE_DIR)
sys.path.append(utils)
print("utils is :{}".format(utils))

from utils.crypto.handle_getKline import get_data_Xprice

symbol_price = ['BTC', 'ETH', 'DOT', 'LINK', 'FIL', 'OP', 'SOL', 'ENS', 'NEAR', 'PEOPLE', 'SNX',
                'DYDX', 'STX', 'DASH', 'LDO', 'SAND', 'APE', 'MATIC', 'DOGE', 'ICP', 'APT', 'ADA', 'MAGIC',
                'MINA', 'MANTA', 'ATOM', 'PYTH', 'BLUR', 'ALT', 'TIA', 'SEI']
# symbol_price = ['BTC']
costPricedic = {'BTC': 21328, 'ETH': 1588, 'DOT': 7, 'LINK': 6.5, 'FIL': 4.5, 'OP': 3.22, 'SOL': 64, 'ENS': 20,
                'NEAR': 1.1, 'PEOPLE': 0.0285, 'SNX': 3.8, 'DYDX': 1.96,
                'STX': 0.49, 'DASH': 30, 'LDO': 3.05, 'SAND': 0.7, 'APE': 1.28, 'MATIC': 0.78, 'DOGE': 0.0916,
                'ICP': 3.52, 'APT': 8.7, 'ADA': 0.26, 'MAGIC': 1.24,
                'MINA': 0.66, 'MANTA': 2.55, 'ATOM': 7.1, 'PYTH': 0.34, 'BLUR': 0.62, 'ALT': 0.35, 'TIA': 15,
                'SEI': 0.59}


def run_get_current_Xprice1():
    send_ding_msgs("日期是:{},中长线持仓成本价:{}".format(str(datetime.datetime.now().date()), costPricedic), myself='alvin')
    X = 2
    get_data_Xprice(symbol_price, costPricedic, str(datetime.datetime.now().date()), X)


def run_get_current_Xprice2():
    X = 3
    get_data_Xprice(symbol_price, costPricedic, str(datetime.datetime.now().date()), X)


def run_get_current_Xprice3():
    X = 4
    get_data_Xprice(symbol_price, costPricedic, str(datetime.datetime.now().date()), X)


def run_get_current_Xprice4():
    X = 5
    get_data_Xprice(symbol_price, costPricedic, str(datetime.datetime.now().date()), X)


def run_get_current_Xprice5():
    X = 6
    get_data_Xprice(symbol_price, costPricedic, str(datetime.datetime.now().date()), X)


def run_get_current_Xprice6():
    X = 7
    get_data_Xprice(symbol_price, costPricedic, str(datetime.datetime.now().date()), X)


def run_get_current_Xprice7():
    X = 8
    get_data_Xprice(symbol_price, costPricedic, str(datetime.datetime.now().date()), X)


def run_get_current_Xprice8():
    X = 9
    get_data_Xprice(symbol_price, costPricedic, str(datetime.datetime.now().date()), X)


def run_get_current_Xprice9():
    X = 10
    get_data_Xprice(symbol_price, costPricedic, str(datetime.datetime.now().date()), X)


def run_get_current_Xprice19():
    X = 20
    get_data_Xprice(symbol_price, costPricedic, str(datetime.datetime.now().date()), X)


if __name__ == '__main__':
    run_get_current_Xprice1()
    run_get_current_Xprice2()
    # run_get_current_Xprice3()
    # run_get_current_Xprice4()
    # run_get_current_Xprice5()
    # run_get_current_Xprice9()
