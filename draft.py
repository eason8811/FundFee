import asyncio
import json
import time

from BinanceAPI import BinanceAPI


base_url_spot = 'https://api.binance.com'
base_url_coin = 'https://dapi.binance.com'
api_key = 'i7F6rx3Tcz6eJlSVzBc4dpV6qyszCiCOIpSz7gv9mdyq9UjVizrlu2kkmlvUIJSw'
secret_key = 'mwU7KCworFZ17WIOqRuGaRmtwT3nnUDBhtg8HQf9CHFB7KVSxev0Rwym5mgfWjDx'

spot_api = BinanceAPI(base_url_spot, api_key, secret_key)
coin_api = BinanceAPI(base_url_coin, api_key, secret_key)

symbols = ['WIFUSD_PERP']

for symbol in symbols:
    body = {
        'type': 'MAIN_CMFUTURE',
        'asset': 'EOS',
        'amount': 0.4,
        'timestamp': int(time.mktime(time.localtime()))*1000,
    }

    response = spot_api.api('POST', '/sapi/v1/asset/transfer', body)
    print(response)