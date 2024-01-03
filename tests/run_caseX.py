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
utils = os.path.join(BASE_DIR,'utils')
sys.path.append(BASE_DIR)
sys.path.append(utils)
print("utils is :{}".format(utils))

from utils.crypto.handle_getKline import  get_data_Xprice

def run_get_current_Xprice():
    # symbol_price =  ['BTC', 'ETH']
    symbol_price =  ['BTC', 'ETH', 'DOT', 'FIL', 'LINK' , 'LTC', 'NEAR', 'SOL', 'DASH', 'SAND', 'AR', 'APE',
                 'SNX', 'RAY', 'MINA', 'ICP', 'DYDX', 'NEO', 'MOVR', 'ADA', 'RNDR', 'STX', 'MAGIC', 'GLMR', 'C98', 'ATOM']
    X = 3
    get_data_Xprice(symbol_price,str(datetime.datetime.now().date()),X)

def run_get_current_Xprice5():
    # symbol_price =  ['BTC', 'ETH']
    symbol_price =  ['BTC', 'ETH', 'DOT', 'FIL', 'LINK' , 'LTC', 'NEAR', 'SOL', 'DASH', 'SAND', 'AR', 'APE',
                 'SNX', 'RAY', 'MINA', 'ICP', 'DYDX', 'NEO', 'MOVR', 'ADA', 'RNDR', 'STX', 'MAGIC', 'GLMR', 'C98', 'ATOM']
    X = 5
    get_data_Xprice(symbol_price,str(datetime.datetime.now().date()),X)


if __name__ == '__main__':
    run_get_current_Xprice()