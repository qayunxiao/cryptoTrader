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

from utils.crypto.handle_getKline import get_data_price
from process_data.symbol_price_history import get_history_data


def run_get_current_price():
    # symbol_price =  ['BTC', 'ETH']
    symbol_price = ['BTC','ETH','DOT','LINK','FIL','OP','LTC','SOL','ENS','NEAR','PEOPLE','SNX',
                    'DYDX','STX', 'DASH','LDO','SAND','APE','MATIC','DOGE','ICP','APT','ADA','MAGIC',
                    'MINA','MANTA','ATOM','PYTH','BLUR','ALT','TIA','SEI']
    get_data_price(symbol_price,str(datetime.datetime.now().date()))


def run_get_history_data():
    symbol_price_history = ['BTC','ETH','DOT','FIL','LINK','LTC','ICP','SNX','LINK','UNI']
    get_history_data(symbol_price_history)



if __name__ == '__main__':
    run_get_current_price()
    # time.sleep(20)
    run_get_history_data()