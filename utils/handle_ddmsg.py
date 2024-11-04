# -*- coding: utf-8 -*-
# -------------------------
# @Time    :  2023/6/27 9:11
# @Author  : alvin
# @Description:  发送钉钉消息
# -------------------------
import configparser
import datetime
import hmac
import hashlib
import base64
import urllib.parse

from handle_log import log
from utils.handle_path import config_path, get_newlogfile
import requests
import json
from urllib3 import encode_multipart_formdata
import time


def send_ding_msg_byfilepath(filepath):

    """发送钉钉群消息"""
    global msg
    print("config_path", config_path)
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8-sig")
    secret = config.get("dingding", 'SECRET')
    access_token = config.get("dingding", 'ACCESS_TOKEN')

    headers = {'Content-Type': 'application/json', "Charset": "UTF-8"}
    # 这里替换为复制的完整 webhook 地址
    prefix = "https://oapi.dingtalk.com/robot/send?access_token={}".format(access_token)

    timestamp = str(round(time.time() * 1000))
    # 这里替换为自己复制过来的加签秘钥
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    url = f'{prefix}&timestamp={timestamp}&sign={sign}'
    print("filepath :{}".format(filepath))
    with open(filepath,"r",encoding="utf-8") as file:
        msg_tmp = file.readlines()
        # print("msg_tmp",len(msg_tmp))
        # print("msg_tmp[2]",msg_tmp[17][54:])

    try:
        msg = "1:" + msg_tmp[6][64:] + "2:大饼" + msg_tmp[8][53:]+msg_tmp[11][54:]+msg_tmp[12][53:]+ "3:以太" + msg_tmp[14][54:]+msg_tmp[17][54:]+msg_tmp[18][53:]
    # 钉钉消息格式，其中 msg 就是我们要发送的具体内容
    except SyntaxError as e:
        print("except:",e)
        print("可能文件数据不够")
        msg="这世界有太多的烟火 这世界有太多的啰嗦 全部都一笑而过,我就是我，颜色不一样的火--by alvin bot"
    finally:
        data = {
            "at": {
                "isAtAll": False
            },
            "text": {
                "content": msg
            },
            "msgtype": "text"
        }
        log.info("send_ding_msg_byfilepath msg is:{}".format(msg))
        return requests.post(url=url, data=json.dumps(data), headers=headers).text

def send_ding_msgs(msg,myself=None):
    # print("config_path", config_path)
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8-sig")
    headers = {'Content-Type': 'application/json', "Charset": "UTF-8"}
    if myself is None:
        secret = config.get("dingding", 'SECRET')
        # 这里替换为复制的完整 webhook 地址
        send_access_token = config.get("dingding", 'ACCESS_TOKEN')
    else:
        send_access_token = config.get("dingding", 'ACCESS_TOKEN_MYSELF')
        # 这里替换为自己复制过来的加签秘钥
        secret = config.get("dingding", 'SECRET_MYSELF')
    prefix = "https://oapi.dingtalk.com/robot/send?access_token={}".format(send_access_token)
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = f'{prefix}&timestamp={timestamp}&sign={sign}'

# 钉钉消息格式，其中 msg 就是我们要发送的具体内容
    data = {
        "at": {
            "isAtAll": False
        },
        "text": {
            "content": msg
        },
        "msgtype": "text"
    }
    log.info("msg is:{}".format(msg))
    return requests.post(url=url, data=json.dumps(data), headers=headers).text


if __name__ == "__main__":
    pass
    # # 填写你的钉钉机器人secret和access_token
    # attachmentFile = "D:\Sourcetree\yunxiao\cryptoTrader\log\crypto_20240223_0930.log"
    # print("attachmentFile",attachmentFile)
    # send_ding_msg_byfilepath(attachmentFile)
    # send_ding_msgs("各位vip群友，今天是元宵佳节，龙年元宵特别圆，圆了你的梦想，币圈稳赚，希望大家事事随缘，节日快乐！")
    # send_ding_msgs("alvin bot all ")
    # send_ding_msgs("alvin bot all ",myself='alvin')
    symbol_price_history = ['BTC', 'ETH']
    baibeisymbol_price = {'IOTX':0.038,'ZKF':0.01,'PYTH':0.4,'BONK':0.0000099,'BAKE':0.45,'MUBI':0.13,'SATS':0.00000075,'ONDO':0.32,'SEI':0.6}
    # send_ding_msgs("百倍币持仓币种数量:{},成本价:{}".format(len(baibeisymbol_price), baibeisymbol_price))
    send_ding_msgs("百倍币持仓币种数量:{},成本价:{}".format(len(baibeisymbol_price), baibeisymbol_price),myself='alvin')