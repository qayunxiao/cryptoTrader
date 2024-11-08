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
# print("process_data is :{}".format(process_data))
from public import math_ceil_float
from utils.handle_ddmsg import send_ding_msgs
from utils.crypto.handle_getKline import get_data_Xprice, get_data_price, get_data_pricepercentage, getCostamount
from process_data.symbol_price_history import get_history_data


class run_priceX():

    def __init__(self):
        self.today_price_list = [] #通过接口回写,根据币安的接口，数据是 持仓币种列表 的币种
        self.sumTotaltokennum = []
        # self.symbol_price_history = ['BTC', 'ETH', 'DOT', 'FIL', 'LINK', 'UNI']
        self.symbol_price_history = ['BTC', 'ETH'] #大饼和山寨的历史数据分析
        self.baibeisymbol_price = {'ONDO':0.32,'ZKF':0.01,'BONK':0.0000099,'BAKE':0.45}
        # 持仓币种列表
        self.symbol_price =['BTC','ETH','BNB', 'BLUR', 'STORJ', 'STX', 'GALA', 'PYTH', 'UNI', 'SOL', 'FIL', 'SUI', 'TIA', 'CKB', 'LINK', 'AUCTION', 'ALT', 'CAKE', 'MANTA', 'RIF', 'IMX', 'WLD', 'AR', 'XAI', 'BIGTIME', 'ARB', 'DASH', 'IOTX' , 'PYTH', 'BONK', 'BAKE','1000SATS', 'SEI' , 'OP', 'SOL', 'ENS', 'NEAR', 'SNX', 'LDO', 'ZEN', 'AAVE', 'SAND', 'APE', 'ICP', 'PEOPLE', 'DOGE', 'DYDX', 'NEO', 'ADA', 'APT', 'MAGIC', 'GLMR', 'MINA','ASTR']
        # 'GPT', 'ZETA', 'LOOKS', 'HONEY'
        # self.symbol_price =['BTC','ETH','BNB', 'BLUR', 'STORJ', 'STX', 'GALA', 'PYTH', 'UNI', 'SOL', 'FIL', 'SUI', 'TIA', 'CKB', 'LINK', 'AGIX', 'AUCTION', 'ALT', 'CAKE', 'MANTA', 'RIF', 'IMX', 'WLD', 'AR', 'XAI', 'BIGTIME', 'GPT', 'ZETA', 'LOOKS', 'HONEY', 'ARB', 'DASH', 'IOTX', 'ZKF', 'PYTH', 'BONK', 'BAKE', 'MUBI', 'SATS', 'ONDO', 'SEI', 'HNT', 'CHAX', 'OP', 'SOL', 'ENS', 'NEAR', 'MATIC', 'SNX', 'LDO', 'ZEN', 'AAVE', 'SAND', 'APE', 'ICP', 'PEOPLE', 'DOGE', 'DYDX', 'NEO', 'ADA', 'APT', 'MAGIC', 'GLMR', 'MINA', 'OKB', 'ASTR', 'CSPR', 'ZBC']
        self.sumTotalAccountCost = 0
        self.sumTotalAccountMarketvalue = 0      
        self.sumAccountFloatinglossToken = [] #所有账户浮亏列表

        # 持仓小号1 c
        self.costPricedic = {'BTC': 21328, 'ETH': 1588, 'DOT': 7, 'LINK': 6.5, 'FIL': 4.5, 'OP': 3.22, 'SOL': 64,
                             'ENS': 20,'NEAR': 1.1, 'PEOPLE': 0.0285, 'SNX': 3.8, 'DYDX': 1.96,
                             'STX': 0.49, 'DASH': 30, 'LDO': 3.05, 'SAND': 0.7, 'APE': 1.28,
                             'DOGE': 0.0916, 'APT': 8.7, 'ADA': 0.26, 'MAGIC': 1.24,
                             'MANTA': 2.55, 'ATOM': 7.1, 'PYTH': 0.34, 'BLUR': 0.62, 'ALT': 0.35,'TIA': 15,'SEI': 0.59}

        self.costPricecountxiaohao1 = [{'BTC':[24920,0.5]},{'BTC':[25800,0.9]},{'BTC':[16000,0.15]},{'BTC':[15800,0.6]},{'BTC':[16800,0.76]},{'BTC':[21999,0.5]},{'BTC':[21700,0.4]},{'BTC':[21550,0.4]},{'BTC':[23450,0.4]},{'BTC':[23618,0.4]},{'BTC':[21200,0.5]},{'BTC':[20370,0.16655]},{'BTC':[21518,0.1]},{'BTC':[19955,0.3152]},{'ETH':[1484,10]},{'ETH':[1588,10]},{'ETH':[1975,2.7]},{'ETH':[2477,6]},{'ETH':[2500,4]},{'UNI':[8.66,1000]},{'FIL':[5.37,1900]},{'SOL':[90.73,92.2]},{'LINK':[6,500]},{'LINK':[15,50]},{'NEAR':[1.16,1158]},{'OP':[2.8,3350]},{'PYTH':[0.47,17732]} ,{'STX':[2.07,5971]},{'ENS':[16.84,365]},{'SNX':[3.36,1999]},{'DYDX':[2.84,1500]},{'GALA':[0.0275,72727]},{'PEOPLE':[0.0285,100000]},{'APE':[1.62,1000]},{'APE':[1.28,1075]},{'LTC':[85,30]},{'SUI':[1.72,872]},{'SUI':[1.48,100]},{'DASH':[30,76]},{'DOGE':[0.0916,10917]},{'SAND':[0.3095,646]},{'SAND':[0.7,3000]},{'SAND':[0.493,1334]},{'DASH':[30,75]},{'DOGE':[0.0916,10922]},{'DOGE':[0.14,1110]},{'ALT':[0.34,7042]}  ,{'ADA':[0.26,904]}]
        self.costPricecountxiaohao2 = [{'BNB': [306, 7]}, {'BNB': [280, 10]}, {'BNB': [366, 8]}, {'BNB': [377, 6.3]},{'ARKM': [2.5, 5294]},{'TIA': [12.47, 719]},{'FET': [2.46, 2283]}  , {'WIF': [3.69, 1047]},{'ENS': [20, 182]} , {'ETHFI': [5.35, 200]}]
        self.costPricecountOlStack1 = [{'DOT':[7.06,3925.00]},{'CAKE':[5.13,1147.00]},{'ATOM':[10.00,480.00]},{'ATOM':[9.39,192.59]},{'TIA':[15.00,70.00]},{'MANTA':[1.60,500.00]},{'MANTA':[2.60,20.00]},{'MANTA':[2.93,420.00]},{'MANTA':[2.86,1072.00]},{'MANTA':[2.8,408.00]},{'ZKF':[0.01,94730.00]},{'ZKF':[0.01,72833.00]},{'PYTH':[0.40,6180.00]},{'PYTH':[0.50,80]},{'SOL':[90.00,3.00]},{'ETH':[2300.00,1.04]},{'ETH':[2300.00,1.04]},{'ETH':[2300.00,1.09]},{'BTC ':[41000.00,0.08]}]

    def run_get_history_data(self):
        get_history_data(self.symbol_price_history)

    def run_get_current_price(self):
        print("run_get_current_price is running....")
        get_data_price(self.symbol_price, str(datetime.datetime.now().date()), self.today_price_list)
        send_ding_msgs("中长线持仓成本价:{}".format(self.costPricedic))
        send_ding_msgs("日期是:{},百倍币持仓币种数量:{},成本价:{}".format(str(datetime.datetime.now().date()),len(self.baibeisymbol_price), self.baibeisymbol_price,myself='alvin'))
        # send_ding_msgs("日期是:{},百倍币持仓币种数量:{},成本价:{}".format(str(datetime.datetime.now().date()),len(self.baibeisymbol_price), self.baibeisymbol_price),myself='alvin')

    def run_get_current_Xprice(self):
        print("run_get_current_Xprice is running....")
        get_data_pricepercentage(self.symbol_price, self.costPricedic, self.today_price_list)
        X_List = [4,5,6,7,8,9,12,15,20]
        for x in X_List:
            get_data_Xprice(self.symbol_price, self.costPricedic, x, self.today_price_list)
        print("run_get_current_Xprice is end !")

    def run_get_current_earnings(self):
        print("run get_current_earnings is running....")
        AccountCost1,AccountMarketvalue1,AccountFloatingloss1 = getCostamount(self.costPricecountxiaohao1, self.today_price_list ,"xiaohao1",self.sumTotalAccountCost,self.sumTotalAccountMarketvalue,self.sumTotaltokennum)
        AccountCost2,AccountMarketvalue2,AccountFloatingloss2 = getCostamount(self.costPricecountxiaohao2, self.today_price_list,"xiaohao2",AccountCost1,AccountMarketvalue1,self.sumTotaltokennum )
        AccountCost3,AccountMarketvalue3,AccountFloatingloss3 = getCostamount(self.costPricecountOlStack1, self.today_price_list,"Stack",AccountCost2,AccountMarketvalue2,self.sumTotaltokennum )
        # 涨幅率=（现价data[1]-原价(costPricedic[symbol]])）/ 原价(costPricedic[symbol]]) * 100%
        increase_allAccount = (AccountMarketvalue3 - AccountCost3) / AccountCost3
        percentage_allAccount = "{:.2%}".format(increase_allAccount)
        time.sleep(30)
        self.sumAccountFloatinglossToken = AccountFloatingloss1 + AccountFloatingloss2 + AccountFloatingloss3
        if len(self.sumAccountFloatinglossToken) > 0:
            unique_coins = set(dic for d in self.sumAccountFloatinglossToken for dic in d)
            coin_count = len(unique_coins)
        else:
            coin_count = 0

        print("所有账户汇总持仓品种数量:{},成本U:{},持仓市值U:{},总盈亏U：{},汇总盈亏率:{},浮亏币种数:{},浮亏Token汇总:{}".format(len(list(set(self.sumTotaltokennum))),math_ceil_float(AccountCost3), math_ceil_float(AccountMarketvalue3),math_ceil_float(AccountMarketvalue3-AccountCost3),percentage_allAccount,coin_count,self.sumAccountFloatinglossToken))
        send_ding_msgs("所有账户汇总持仓品种数量:{},成本U:{},持仓市值U:{},总盈亏U：{},汇总盈亏率:{},浮亏币种数:{},浮亏Token汇总:{}".format(len(list(set(self.sumTotaltokennum))),math_ceil_float(AccountCost3), math_ceil_float(AccountMarketvalue3),math_ceil_float(AccountMarketvalue3-AccountCost3),percentage_allAccount,coin_count,self.sumAccountFloatinglossToken),myself='alvin')
        print("run get_current_earnings is end !")



if __name__ == '__main__':
    run_x = run_priceX()
    # run_x.run_get_history_data()
    run_x.run_get_current_price()
    run_x.run_get_current_Xprice()
    run_x.run_get_current_earnings()
