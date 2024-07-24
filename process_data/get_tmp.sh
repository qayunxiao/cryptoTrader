#!/bin/bash

while true; do
    # 获取当前价格
    price=$(curl -s 'https://api.binance.com/api/v3/depth?symbol=ETHUSDT&limit=1' | jq -r '.asks[0][0]')
    # 将价格格式化为保留两位小数
    formatted_price=$(printf "%.2f" $price)
    # 输出当前时间和格式化后的价格，覆盖前一次输出
    printf "\r$(date '+%Y-%m-%d %H:%M:%S') - Price: $formatted_price"
    # 等待 5 秒
    sleep 5
done