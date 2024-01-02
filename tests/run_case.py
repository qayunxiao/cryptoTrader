# -*- coding: utf-8 -*-
# -------------------------
# @Time    :  2024/1/2 12:04
# @Author  : alvin
# @Description:  func
# -------------------------
import datetime

from crypto.handle_getKline import get_data_price
from process_data.symbol_price_history import get_history_data


def run_get_current_price():
    symbol_price =  ['BTC', 'ETH']
    symbol_ls =  ['BTC', 'ETH', 'DOT', 'FIL', 'LINK', 'LINK', 'LTC', 'NEAR', 'SOL', 'DASH', 'SAND', 'AR', 'APE',
                 'SNX', 'RAY', 'MINA', 'ICP', 'DYDX', 'NEO', 'MOVR', 'ADA', 'RNDR', 'STX', 'MAGIC', 'GLMR', 'C98', 'ATOM', 'MAGIC']
    get_data_price(symbol_price,str(datetime.datetime.now().date()))


def run_get_history_data():
    symbol_price_history =  ['BTC', 'DOT', 'ETH', 'ICP', 'LINK', 'UNI']
    get_history_data(symbol_price_history)



if __name__ == '__main__':
    # run_get_current_price()
    run_get_history_data()