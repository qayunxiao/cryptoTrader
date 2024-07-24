#!/bin/bash

# 无限循环
while true; do
    # 使用 curl 和 jq 获取ETHUSDT的数据
    eth_value=$(curl -s 'https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=1' | jq -r '.asks[0][0]')

    # 检查curl命令是否成功
    if [ $? -eq 0 ]; then
        # 使用printf格式化输出，保留两位小数
        formatted_value=$(printf "%.2f" "$eth_value")
        echo -ne "\033]0;E: $formatted_value\007"
    else
        echo "Failed to fetch data"
    fi

    # 每10秒钟执行一次
    sleep 10
done
