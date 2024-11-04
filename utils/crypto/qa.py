# -*- coding: utf-8 -*-
# -------------------------
# @Time    :  2024/2/22 11:37
# @Author  : alvin
# @Description:  func
# -------------------------


today_price_list = [['BTC', 51521.24], ['ETH', 2930.83], ['DOT', 7.359], ['LINK', 18.339], ['FIL', 7.287], ['OP', 3.672], ['SOL', 102.96], ['ENS', 21.68], ['NEAR', 3.159], ['PEOPLE', 0.02836], ['SNX', 3.46], ['DYDX', 2.925], ['STX', 2.5864], ['DASH', 29.06], ['LDO', 3.004], ['SAND', 0.485], ['APE', 1.649], ['MATIC', 0.9286], ['DOGE', 0.08384], ['ICP', 12.957], ['APT', 9.0172], ['ADA', 0.5853], ['MAGIC', 1.2821], ['MINA', 1.2604], ['MANTA', 3.1414], ['ATOM', 9.808], ['PYTH', 0.5277], ['BLUR', 0.6865], ['ALT', 0.5016], ['TIA', 16.959], ['SEI', 0.8277]]
# for data in today_price_list:
#     # print(data)
#     if 'ATOM' in data:
#         print(data[1])
# X_List = [2,3,4]
# for x in X_List:
#     print(x)

lista = ['BNB','BNB','BLUR','STORJ','STX','STX','gala','pyth','pyth','uni','SOL','SOL','fil','SUI','tia','ckb','link','link','agix','AUCTION','ALT','CAKE','MANTA','RIF','IMX','wld','AR','xai','Bigtime','GPT','ZETA','LOOKS','honey','ARB','uni','CAKE','dash','IOTX','ZKF','PYTH','BONK','BAKE','MUBI','SATS','ONDO','SEI','HNT','CHAX','link','link','OP','sol','sol','ENS','NEAR','STX','STX','MATIC','MATIC','SNX','SNX','SNX','LDO','LDO','dash','zen','aave','SAND','SAND','APE','APE','ICP','PEOPLE','DOGE','DYDX','NEO','ada','APT','APT','MAGIC','BLUR','ALT','SEI','STORJ','GLMR','MINA','IMX','OKB','ASTR','CSPR','ZBC' ]
new_lst = [x for i, x in enumerate(lista) if x not in lista[:i]]
all= []
for i in new_lst:
    all.append(i.upper())
print(all)
a=[{'LDO': {'数量': 300.0, '成本价': 3.32, '总成本价': 996.0, '最新价': 3.247, '最新持仓价值': 974.1, '盈亏U': -21.89, '盈亏率': '-2.20%'}}, {'TIA': {'数量': 114.0, '成本价': 16.8, '总成本价': 1915.2, '最新价': 15.8, '最新持仓价值': 1801.2, '盈亏U': -114.0, '盈亏率': '-5.95%'}}, {'STX': {'数量': 677.0, '成本价': 2.95, '总成本价': 1997.15, '最新价': 2.9305, '最新持仓价值': 1983.95, '盈亏U': -13.2, '盈亏率': '-0.66%'}}, {'CAKE': {'数量': 1147.0, '成本价': 5.13, '总成本价': 5884.11, '最新价': 3.92, '最新持仓价值': 4496.24, '盈亏U': -1387.87, '盈亏率': '-23.59%'}}]

# 示例调用
# getCostamount(my_costPricecountlist, my_today_price_list)

if __name__ == '__main__':
    print(len(a))