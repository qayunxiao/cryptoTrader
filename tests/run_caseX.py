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
sys.path.append(BASE_DIR)
sys.path.append(utils)
print("utils is :{}".format(utils))

from utils.crypto.handle_getKline import get_data_Xprice

# symbol_price =  ['BTC', 'ETH']
symbol_price = ['BTC', 'ETH', 'DOT', 'LINK', 'FIL', 'OP', 'LTC', 'SOL', 'ENS', 'NEAR', 'PEOPLE', 'SNX',
                'DYDX', 'STX', 'DASH', 'LDO', 'SAND', 'APE', 'MATIC', 'DOGE', 'ICP', 'APT', 'ADA', 'MAGIC',
                'MINA', 'MANTA', 'ATOM', 'PYTH', 'BLUR', 'ALT', 'TIA', 'SEI']


def run_get_current_Xprice2():
    X = 2
    get_data_Xprice(symbol_price, str(datetime.datetime.now().date()), X)


def run_get_current_Xprice3():
    X = 3
    get_data_Xprice(symbol_price, str(datetime.datetime.now().date()), X)


def run_get_current_Xprice4():
    X = 4
    get_data_Xprice(symbol_price, str(datetime.datetime.now().date()), X)


def run_get_current_Xprice5():
    X = 5
    get_data_Xprice(symbol_price, str(datetime.datetime.now().date()), X)

def run_get_current_Xprice6():
    X = 6
    get_data_Xprice(symbol_price, str(datetime.datetime.now().date()), X)

def run_get_current_Xprice7():
    X = 7
    get_data_Xprice(symbol_price, str(datetime.datetime.now().date()), X)

def run_get_current_Xprice8():
    X = 8
    get_data_Xprice(symbol_price, str(datetime.datetime.now().date()), X)

def run_get_current_Xprice9():
    X = 9
    get_data_Xprice(symbol_price, str(datetime.datetime.now().date()), X)

def run_get_current_Xprice10():
    X = 10
    get_data_Xprice(symbol_price, str(datetime.datetime.now().date()), X)


if __name__ == '__main__':
    run_get_current_Xprice2()
    run_get_current_Xprice3()
    run_get_current_Xprice4()
    run_get_current_Xprice5()
    # run_get_current_Xprice10()
