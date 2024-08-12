import asyncio
import json
import time
import matplotlib.pyplot as plt

from BinanceAPI import BinanceAPI

base_url_spot = 'https://api.binance.com'
base_url_coin = 'https://dapi.binance.com'
api_key = 'i7F6rx3Tcz6eJlSVzBc4dpV6qyszCiCOIpSz7gv9mdyq9UjVizrlu2kkmlvUIJSw'
secret_key = 'mwU7KCworFZ17WIOqRuGaRmtwT3nnUDBhtg8HQf9CHFB7KVSxev0Rwym5mgfWjDx'

spot_api = BinanceAPI(base_url_spot, api_key, secret_key)
coin_api = BinanceAPI(base_url_coin, api_key, secret_key)

symbols = ['WIFUSD_PERP']

with open('cache.txt', 'r') as f:
    data = list(map(lambda x: float(x), f.read().strip().split('\n')))
plt.plot(data)
print(f'max: {max(data)}, min: {min(data)}')
plt.show()

# for symbol in symbols:
#     body = {
#         'type': 'MAIN_CMFUTURE',
#         'asset': 'EOS',
#         'amount': 0.4,
#         'timestamp': int(time.mktime(time.localtime()))*1000,
#     }
#
#     response = spot_api.api('POST', '/sapi/v1/asset/transfer', body)
#     print(response)

# for symbol in symbols:
#     body = {
#         'symbol': symbol.replace('_PERP', 'T'),
#         'orderId': 1930812968,
#         'timestamp': int(time.mktime(time.localtime())) * 1000,
#     }
#     response = spot_api.api('GET', '/api/v3/order', body)
#     print(response)
#     buy_spot_price = float(response['price'])
#
#     body = {
#         'symbol': symbol,
#         'orderId': 90291953,
#         'timestamp': int(time.mktime(time.localtime())) * 1000,
#     }
#     response = coin_api.api('GET', '/dapi/v1/order', body)
#     print(response)
#     sell_coin_price = float(response['avgPrice'])
#
#     print(f'实际成交价差：{round((sell_coin_price - buy_spot_price) / buy_spot_price * 100, 4)}%')
