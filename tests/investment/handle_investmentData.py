# -*- coding: utf-8 -*-
# @Time    : 2023/3/9 17:06
# @Author  : alvin
# @File    : handle_investmentData.py
# @Software: PyCharm

import  numpy as np
import matplotlib.pyplot as plt
# import matplotlib.finance as mpf

def testBi():
    #sma 5
    filename="./hasbtc.csv"
    price,count,cost  = np.loadtxt(
        fname=filename,
        delimiter=',',
        usecols=(0,1,2),
        unpack=True
    )
    print(price,count,cost)
    N = 2#5日均线
    weights = np.ones(N) /N
    print(weights)
    sma = np.convolve(weights,price)[N-1:-N+1]
    print(sma,type(sma))
    plt.plot(sma,linewidth=5)
    # plt.plot(cost,linewidth=2)
    plt.show()
#获取持仓数量和成本均价
def testhasBiprice(filename=".has/btcbak.csv"):
    price,count,cost  = np.loadtxt(
        fname=filename,
        delimiter=',',
        usecols=(0,1,2),
        unpack=True
    )
    print("testBiprice cost total  is :{}".format(np.sum(cost)))
    print("testBiprice count total is :{}".format(np.sum(count)))
    print("testBiprice avg is  :{}".format((np.sum(cost))/np.sum(count)))
# print("testBiprice avg total is :{}".format( (np.sum(cost)/np.sum(count)) ))
#     plt.ylim(14000, 25000) # 设置y轴刻度范围
    # plt.plot(count,price,  color='green', marker='o', linestyle='solid')
    # plt.title('btc')
    # plt.xlabel('count')
    # plt.ylabel('Price')
    # plt.show()


def testBijihuaprice(filename="./btcbak.csv"):
    price,count  = np.loadtxt(
        fname=filename,
        delimiter=',',
        usecols=(0,1),
        unpack=True
    )
    # print("testBijihuaprice price total  is :{}".format(np.sum(price)))
    print("数量count total is :{}".format(np.sum(count)))
    print("资金cost is :{}".format( np.sum(price*count)))#80000
    print("平均价 avg total is :{}".format( ((np.sum(price*count))/np.sum(count)) ))
    # plt.ylim(14000, 25000) # 设置y轴刻度范围
    # plt.plot(count,price,  color='green', marker='o', linestyle='solid')
    # plt.title('btc')
    # plt.xlabel('count')
    # plt.ylabel('Price')
    # plt.show()


if __name__ == '__main__':
    # testReadFile()
    path ="./hasbtc.csv"
    testhasBiprice(path)
    path1 ="./jihua_eth.csv"
    testBijihuaprice(path1)
