# -*- coding: UTF-8 -*-
import csv
import datetime
import os
import platform
import random
import sys

import ccxt
import pandas as pd
import time

# Python 3.5.3+ 中支持使用 asyncio 和 async/await 的并发异步模式
# import ccxt.async_support as ccxt
from handle_ddmsg import send_ding_msgs
from handle_log import log
from utils.handle_path import project_path, data_ccxt_path


def get_data(symbol='BTC/USDT'):
    tmp_data_ccxt_path = os.path.join(project_path, 'data', 'ccxt_binance_tmpdata')
    tmp_filename = symbol.split('/')[0] + '_tmp.csv'
    tmp_file_path = os.path.join(tmp_data_ccxt_path, tmp_filename)
    # print("tmp_file_path",tmp_file_path)
    history_ccxt_tmppath = os.path.join(project_path, 'data', 'ccxt_binance_historydata')
    history_filename = symbol.split('/')[0] + '_history.csv'
    history_data_path = os.path.join(history_ccxt_tmppath, history_filename)
    # print("history_data_path",history_data_path)

    my_ccxt_tmppath = os.path.join(project_path, 'data', 'ccxt_binance_data')
    my_filename = symbol.split('/')[0] + '.csv'
    my_data_path = os.path.join(my_ccxt_tmppath, my_filename)
    # print("my_data_path",my_data_path)

    delay = 3  # seconds https://api.binance.com/api/v3/exchangeInfo
    if "Windows" == platform.system():
        binance_exchange = ccxt.binance({
            'timeout': 15000,
            'enableRateLimit': True,
            'proxies': {'https': "http://127.0.0.1:1082", 'http': "http://127.0.0.1:1081"}
        })
    else:
        binance_exchange = ccxt.binance({
            'timeout': 15000,
            'enableRateLimit': True,
        })

    # symbol = 'BTC/USDT'
    # print("symbol",symbol)
    # 交易所数据结构
    # print('交易所id：', binance_exchange.id,'交易所名称：', binance_exchange.name)
    # print('是否支持共有API：', binance_exchange.has['publicAPI'],'是否支持私有API：', binance_exchange.has['privateAPI'])
    # print('支持的时间频率：', binance_exchange.timeframes,'交易所当前时间：', binance_exchange.iso8601(binance_exchange.milliseconds()))
    # print('最长等待时间(s)：', binance_exchange.timeout / 1000 , '访问频率(s)：', binance_exchange.rateLimit / 1000)
    # 交易所数据结构

    # 加载市场数据
    binance_markets = binance_exchange.load_markets()
    # 支持的交易对
    markets_list = list(binance_markets.keys())

    # 获取全部币种盘口信息
    # for all_symbol in binance_exchange.markets:
    #     #print(binance_exchange.fetch_order_book(all_symbol))
    #     time.sleep(delay)

    # 获取指定交易对市场信息
    btc_usdt_market = binance_markets[symbol]
    #     #print("btc_usdt_market",btc_usdt_market)

    # 获取单个交易对ticker数据fetchTickers
    ticker_data = binance_exchange.fetch_ticker(symbol)
    #     #print("ticker_datamarket",ticker_data)
    # #print('Ticker时刻：', ticker_data['datetime'])
    # #print('Ticker价格：', ticker_data['last'])

    # 转换UTC时间
    # print('Ticker数据开始时间：', binance_exchange.iso8601(ticker_data['info']['openTime']))
    # print('Ticker数据结束时间：', binance_exchange.iso8601(ticker_data['info']['closeTime']))

    # 交易委托账本数据获取
    binance_exchange.fetch_order_book(symbol)
    # 获取上一次访问交易所的时间
    #     binance_exchange.last_response_headers['Date']
    orderbook = binance_exchange.fetch_order_book(symbol)
    # 最高买价
    bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    # 最低卖价
    ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
    # 价差
    spread = (ask - bid) if (bid and ask) else None
    # 市场行情
    # print ('买价：{:.2f}, 卖价：{:.2f}, 价差：{:.2f}'.format(bid, ask, spread))
    # K线数据数据获取
    binance_exchange.fetch_ohlcv(symbol, timeframe='1d')
    if binance_exchange.has['fetchOHLCV']:
        pass
        # print(binance_exchange.fetch_ohlcv(symbol, timeframe='1d'))

    # 1636473600000  1607529600000
    if (((symbol.split('/')[0]) == 'BTC') or ((symbol.split('/')[0]) == 'ETH')):
        kline_data = binance_exchange.fetch_ohlcv(symbol, timeframe='1d', since=1704038400000)
    elif (((symbol.split('/')[0]) == 'DOT')):  # 20211104 历史数据含有
        kline_data = binance_exchange.fetch_ohlcv(symbol, timeframe='1d', since=1704038400000)
    elif (((symbol.split('/')[0]) == 'LTC')):  # 20210510 历史数据含有
        kline_data = binance_exchange.fetch_ohlcv(symbol, timeframe='1d', since=1704038400000)
    elif (((symbol.split('/')[0]) == 'FIL')):  # 20210401 历史数据含有
        kline_data = binance_exchange.fetch_ohlcv(symbol, timeframe='1d', since=1704038400000)
    elif (((symbol.split('/')[0]) == 'AGIX')):  # 之前高点数据单独处理
        kline_data = binance_exchange.fetch_ohlcv(symbol, timeframe='1d', since=1704038400000)
    elif (((symbol.split('/')[0]) == 'SNX')):  #
        kline_data = binance_exchange.fetch_ohlcv(symbol, timeframe='1d', since=1704038400000)
    elif (((symbol.split('/')[0]) == 'LINK')):  #
        kline_data = binance_exchange.fetch_ohlcv(symbol, timeframe='1d', since=1704038400000)
    elif (((symbol.split('/')[0]) == 'SOL')):  #
        kline_data = binance_exchange.fetch_ohlcv(symbol, timeframe='1d', since=1704038400000)
    else:
        kline_data = binance_exchange.fetch_ohlcv(symbol, timeframe='1d', since=1704038400000)

    #  处理数据格式 时间戳毫秒改日期格式
    kline_df = pd.DataFrame(kline_data, columns=["time", "open", "high", "low", "close", "vol"])
    # to_datetime  将时间戳毫秒转日期 -unit='ms'
    kline_df['date'] = pd.to_datetime(kline_df['time'], unit='ms')
    # kline_df = pd.DataFrame(kline_data)
    # print("kline_df_tail",kline_df.tail(2))
    # print("kline_df_head",kline_df.head(2))

    # 存储数据 判断tmp文件是否存在，如果存在就删除
    if os.path.exists(tmp_file_path):  # 判断文件是否存在
        os.remove(tmp_file_path)
        # print("tmp file exists is:",os.path.exists(tmp_file_path))
        time.sleep(1)
        kline_df.to_csv(tmp_file_path, mode="a", index=False, header=True, encoding='utf-8')
    else:
        # print("not exists")
        kline_df.to_csv(tmp_file_path, mode="a", index=False, header=True, encoding='utf-8')
    # print("获取tmp文件:{}成功".format(tmp_file_path))
    # 获取orderbook
    order_book = binance_exchange.fetch_order_book(symbol)
    #     #print("order_book",order_book['bids'])
    print("tmp_file_path is :{}".format(tmp_file_path))
    df1 = pd.read_csv(tmp_file_path)
    # df1["来自文件"] = "tmp"
    print("history_data_path is :{}".format(history_data_path))
    df2 = pd.read_csv(history_data_path)
    # df2["来自文件"] = "history"
    df = pd.concat([df2, df1])
    df.drop_duplicates()  # 数据去重
    df.to_csv(my_data_path, encoding='utf-8')  # 合并历史与tmp文件
    # fr1 = open(history_data_path,'r',encoding='utf-8').read()
    # fr2 = open(tmp_file_path,'r',encoding='utf-8').read()
    # with open(my_data_path,'a',encoding='utf-8') as f:
    #     f.write(fr1)
    #     f.write('\n')
    #     f.write(fr2)
    print("concat_csv {} over ".format(my_data_path))


def concat_csv():
    data_ccxt_path = os.path.join(project_path, 'data', 'ccxt_binance_data')
    f1 = os.path.join(data_ccxt_path, 'BTC.csv')
    f2 = os.path.join(data_ccxt_path, 'BTC_all.csv')
    df1 = pd.read_csv(f1)
    df2 = pd.read_csv(f2)
    df = pd.concat([df2, df1])
    f_my = os.path.join(data_ccxt_path, 'BTC2.csv')
    df.to_csv(f_my, encoding='utf-8')
    # print("concat_csv {} over ".format(f_my))
    # print("kline_df_head",df.head(2))


def get_data_hisroty(symbol, start_date):
    history_ccxt_tmppath = os.path.join(project_path, 'data', 'ccxt_binance_historydata')
    history_filename = symbol.split('/')[0] + '_history.csv'
    history_data_path = os.path.join(history_ccxt_tmppath, history_filename)
    # print("history_data_path is :{}".format(history_data_path))
    delay = 3  # seconds https://api.binance.com/api/v3/exchangeInfo
    if "Windows" == platform.system():
        binance_exchange = ccxt.binance({
            'timeout': 15000,
            'enableRateLimit': True,
            'proxies': {'https': "http://127.0.0.1:1082", 'http': "http://127.0.0.1:1081"}
        })
    else:
        binance_exchange = ccxt.binance({
            'timeout': 15000,
            'enableRateLimit': True,
        })

    # 加载市场数据
    binance_markets = binance_exchange.load_markets()
    symbol = symbol + '/USDT'
    binance_exchange.fetch_order_book(symbol)
    orderbook = binance_exchange.fetch_order_book(symbol)
    # 最高买价
    bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    # 最低卖价
    ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
    # 价差
    spread = (ask - bid) if (bid and ask) else None
    # 市场行情
    # print ('买价：{:.2f}, 卖价：{:.2f}, 价差：{:.2f}'.format(bid, ask, spread))
    # K线数据数据获取1620576000  1664640000000
    binance_exchange.fetch_ohlcv(symbol, timeframe='1d')
    if binance_exchange.has['fetchOHLCV']:
        print(binance_exchange.fetch_ohlcv(symbol, timeframe='1d'))
    since_date = date_to_timestamp(start_date)
    kline_data = binance_exchange.fetch_ohlcv(symbol, timeframe='1d', since=int(since_date))
    # print("kline_data    is :{}".format((kline_data)))
    # print("kline_data  LAST is :{}".format( (kline_data[-1][-2])))

    #  处理数据格式 时间戳毫秒改日期格式
    kline_df = pd.DataFrame(kline_data, columns=["time", "open", "high", "low", "close", "vol"])
    # to_datetime  将时间戳毫秒转日期 -unit='ms'
    kline_df['date'] = pd.to_datetime(kline_df['time'], unit='ms')

    # 存储数据 判断tmp文件是否存在，如果存在就删除
    if os.path.exists(history_data_path):  # 判断文件是否存在
        os.remove(history_data_path)
        # print("tmp file exists is:",os.path.exists(history_data_path))
        time.sleep(2)
        kline_df.to_csv(history_data_path, mode="a", index=False, header=True, encoding='utf-8')
    else:
        # print("not exists")
        kline_df.to_csv(history_data_path, mode="a", index=False, header=True, encoding='utf-8')


def date_to_timestamp(date_str):
    # import datetime
    # date_str = "2022-01-01"
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    timestamp = date_obj.timestamp()
    timestamp = int(timestamp)
    timestamp = str(timestamp)
    timestamp = timestamp + '000'
    print(" timestamp is:{}".format(timestamp))
    return timestamp


def get_data_price(symbol_list, price_date, today_price_list):
    # 获取单一bi种的历史数据
    new_price_date = price_date
    binance_exchange = None
    delay = 3  # seconds https://api.binance.com/api/v3/exchangeInfo
    if "Windows" == platform.system():
        binance_exchange = ccxt.binance({
            'timeout': 15000,
            'enableRateLimit': True,
            'proxies': {'https': "http://127.0.0.1:1082", 'http': "http://127.0.0.1:1081"}
        })
    else:
        binance_exchange = ccxt.binance({
            'timeout': 15000,
            'enableRateLimit': True,
        })

    # 加载市场数据
    binance_markets = binance_exchange.load_markets()
    price_list = []
    price_date = date_to_timestamp(price_date)
    for symbol in symbol_list:
        symbol_usdt = symbol + '/USDT'
        # print("symbol_usdt is :{}".format(symbol_usdt))
        binance_exchange.fetch_order_book(symbol_usdt)
        orderbook = binance_exchange.fetch_order_book(symbol_usdt)
        # 最高买价
        bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
        # 最低卖价
        ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
        # 价差
        spread = (ask - bid) if (bid and ask) else None
        # 市场行情
        # print ('买价：{:.2f}, 卖价：{:.2f}, 价差：{:.2f}'.format(bid, ask, spread))
        # K线数据数据获取1620576000  1664640000000
        binance_exchange.fetch_ohlcv(symbol_usdt, timeframe='1d')
        if binance_exchange.has['fetchOHLCV']:
            # print("fetchOHLCV is :{}".format(binance_exchange.fetch_ohlcv(symbol_usdt, timeframe='1d')))
            kline_data = binance_exchange.fetch_ohlcv(symbol_usdt, timeframe='1d', since=int(price_date))
            # print("symbol is :{} ,close price is :{}".format(symbol,(kline_data[-1][-2])))
            time.sleep(delay)
            #  处理数据格式 时间戳毫秒改日期格式
            kline_df = pd.DataFrame(kline_data, columns=["time", "open", "high", "low", "close", "vol"])
            # to_datetime  将时间戳毫秒转日期 -unit='ms'
            kline_df['date'] = pd.to_datetime(kline_df['time'], unit='ms')
            price_today = kline_data[-1][-2]
            price_list.append([symbol, price_today])
            # log.info("price_today type is :{}".format(type(price_today)))
            today_price_list.append([symbol, price_today])
            log.info("today_price_list is :{}".format(today_price_list))

    if today_price_list is None:
        send_ding_msgs("日期是:{},获取今日报价是空:{},异常退出！".format(new_price_date, today_price_list), myself='alvin')
        sys.exit(-1)
    else:
        # print("日期是:{},价格是:{}".format(new_price_date, price_list))
        # send_ding_msgs("日期是:{},中长线持仓币种与当前价格是:{}".format(new_price_date, price_list))
        send_ding_msgs("日期是:{},中长线持仓币种与当前价格是:{}".format(new_price_date, price_list), myself='alvin')


def get_data_Xprice(symbol_list, costPricedic, X, today_price_list):
    log.info("get_data_Xprice :{} is running ...".format(X - 1))
    if X is None:
        sys.exit(1)
    price_list = []
    for symbol in symbol_list:
        # time.sleep(random.randint(1, 3))
        if symbol in costPricedic:
            for data in today_price_list:
                if symbol in data:
                    if data[1] > (costPricedic[symbol] * X):
                        price_list.append([symbol, data[1], costPricedic[symbol]])
    if not price_list:
        log.info("浮盈{}倍的token是空,符合的{} ".format(X - 1, price_list))
    else:
        log.info("目前浮盈{}倍的token信息:{}".format(X - 1, price_list))
        send_ding_msgs("目前浮盈{}倍的token信息:{}".format(X - 1, price_list), myself='alvin')


def get_data_pricepercentage(symbol_list, costPricedic, today_price_list):
    log.info("get_data get_data_pricepercentage  is running ...")
    price_percentagelist = []
    price_percentagelist_negative = []
    price_percentagelistFlag = False
    # 涨幅率=（现价data[1]-原价(costPricedic[symbol]])）/ 原价(costPricedic[symbol]]) * 100%
    for symbol in symbol_list:
        # time.sleep(random.randint(1, 3))
        if symbol in costPricedic:
            for data in today_price_list:
                if symbol in data:
                    increase = (data[1] - costPricedic[symbol]) / costPricedic[symbol]
                    formatted_percentage = "{:.2%}".format(increase)
                    if increase < 0:
                        price_percentagelistFlag = True
                        price_percentagelist_negative.append([symbol, costPricedic[symbol], data[1], formatted_percentage])
                    else:
                        price_percentagelist.append([symbol, costPricedic[symbol], data[1], formatted_percentage])
    if not price_percentagelist:
        log.info("price_percentagelist is null")
    else:
        if price_percentagelistFlag:
            log.info("目前持仓币种数量:{} ,token盈亏情况{},浮亏的信息是:{}".format(len(price_percentagelist),price_percentagelist,price_percentagelist_negative))
            send_ding_msgs("目前持仓token种类:{} ,浮盈情况{},浮亏是:{}".format(len(price_percentagelist),price_percentagelist,price_percentagelist_negative))
            send_ding_msgs("目前持仓token种类:{} ,浮盈情况{},浮亏是:{}".format(len(price_percentagelist),price_percentagelist,price_percentagelist_negative), myself='alvin')
        else:
            log.info("目前持仓币种数量:{} ,token盈亏情况{},没有任何浮亏！".format(len(price_percentagelist),price_percentagelist))
            send_ding_msgs("目前持仓token种类:{} ,浮盈情况{},没有任何浮亏！".format(len(price_percentagelist),price_percentagelist))
            send_ding_msgs("目前持仓token数量:{} ,浮盈情况{},没有任何浮亏！".format(len(price_percentagelist),price_percentagelist), myself='alvin')


if __name__ == '__main__':
    symbol_list = ['BTC', 'ETH', 'DOT']
    costPricedic = {'BTC': 21328, 'ETH': 1588, 'DOT': 7, 'LINK': 6.5, 'FIL': 4.5, 'OP': 3.22, 'SOL': 64,
                    'ENS': 20,
                    'NEAR': 1.1, 'PEOPLE': 0.0285, 'SNX': 3.8, 'DYDX': 1.96,
                    'STX': 0.49, 'DASH': 30, 'LDO': 3.05, 'SAND': 0.7, 'APE': 1.28, 'MATIC': 0.78,
                    'DOGE': 0.0916,
                    'ICP': 3.52, 'APT': 8.7, 'ADA': 0.26, 'MAGIC': 1.24,
                    'MINA': 0.66, 'MANTA': 2.55, 'ATOM': 7.1, 'PYTH': 0.34, 'BLUR': 0.62, 'ALT': 0.35,
                    'TIA': 15,
                    'SEI': 0.59}
    today_price_list = [['BTC', 62117.81], ['ETH', 3424.5], ['DOT', 6], ['LINK', 19.909], ['FIL', 8.302],
                        ['OP', 3.797], ['SOL', 133.26], ['ENS', 21.44], ['NEAR', 3.987], ['PEOPLE', 0.04369],
                        ['SNX', 4.355], ['DYDX', 3.444], ['STX', 2.9841], ['DASH', 33.14], ['LDO', 3.434],
                        ['SAND', 0.6163], ['APE', 1.962], ['MATIC', 1.0211], ['DOGE', 0.1223], ['ICP', 12.803],
                        ['APT', 11.7371], ['ADA', 0.6779], ['MAGIC', 1.2384], ['MINA', 1.3112], ['MANTA', 2.739],
                        ['ATOM', 11.395], ['PYTH', 0.6691], ['BLUR', 0.7329], ['ALT', 0.47687], ['TIA', 16.83],
                        ['SEI', 0.8515]]

    get_data_pricepercentage(symbol_list, costPricedic, today_price_list)
