# -*- coding: utf-8 -*-
# -------------------------
# @Time    :  2023/6/27 9:11
# @Author  : alvin
# @Description:  发送钉钉消息
# -------------------------
import configparser
import hmac
import hashlib
import base64
import json
import urllib.parse
import time
import requests
from utils.handle_path import config_path, get_newlogfile
import requests
import json
from urllib3 import encode_multipart_formdata
import time


def send_ding_msg_byfilepath(filepath):

    """发送钉钉群消息"""

    print("config_path", config_path)
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8-sig")
    send_secret = config.get("dingding", 'SECRET')
    send_access_token = config.get("dingding", 'ACCESS_TOKEN')

    headers = {'Content-Type': 'application/json', "Charset": "UTF-8"}
    # 这里替换为复制的完整 webhook 地址
    prefix = "https://oapi.dingtalk.com/robot/send?access_token={}".format(send_access_token)
    print("send_secret", send_secret)
    print("prefix", prefix)

    timestamp = str(round(time.time() * 1000))
    # 这里替换为自己复制过来的加签秘钥
    secret = config.get("dingding", 'SECRET')
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    url = f'{prefix}&timestamp={timestamp}&sign={sign}'

    with open(filepath,"r",encoding="utf-8") as file:
        msg_tmp = file.readlines()
    # print("msg_tmp",len(msg_tmp))
    msg=msg_tmp[2]+msg_tmp[5]+msg_tmp[12]+msg_tmp[18]+msg_tmp[2]+msg_tmp[24]

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
    return requests.post(url=url, data=json.dumps(data), headers=headers).text


def send_ding_msgs(msg):
    print("config_path", config_path)
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8-sig")
    send_secret = config.get("dingding", 'SECRET')
    send_access_token = config.get("dingding", 'ACCESS_TOKEN')

    headers = {'Content-Type': 'application/json', "Charset": "UTF-8"}
# 这里替换为复制的完整 webhook 地址
    prefix = "https://oapi.dingtalk.com/robot/send?access_token={}".format(send_access_token)
    print("send_secret", send_secret)
    print("prefix", prefix)

    timestamp = str(round(time.time() * 1000))
# 这里替换为自己复制过来的加签秘钥
    secret = config.get("dingding", 'SECRET')
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

    return requests.post(url=url, data=json.dumps(data), headers=headers).text




if __name__ == "__main__":

    # 填写你的钉钉机器人secret和access_token
    attachmentFile = get_newlogfile()
    print("attachmentFile",attachmentFile)
    msg = '我是rob vip 机器人，欢迎大家进群！'
    send_ding_msg_byfilepath(attachmentFile)
