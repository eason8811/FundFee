from BinanceAPI import BinanceAPI
import time

base_url_spot = 'https://api.binance.com'
base_url_coin = 'https://dapi.binance.com'
api_key = 'i7F6rx3Tcz6eJlSVzBc4dpV6qyszCiCOIpSz7gv9mdyq9UjVizrlu2kkmlvUIJSw'
secret_key = 'mwU7KCworFZ17WIOqRuGaRmtwT3nnUDBhtg8HQf9CHFB7KVSxev0Rwym5mgfWjDx'

spot_api = BinanceAPI(base_url_spot, api_key, secret_key)
coin_api = BinanceAPI(base_url_coin, api_key, secret_key)

symbols = ['WIFUSD_PERP']

while True:
    time.sleep(0.1)
    for symbol in symbols:
        body = {
            'symbol': symbol,
            'limit': 5
        }
        respond = coin_api.api('GET', '/dapi/v1/depth', body)
        buy1 = respond['bids'][0]
        buy2 = respond['bids'][1]
        body = {
            'symbol': symbol.replace('_PERP', '') + 'T',
            'limit': 5
        }
        respond = spot_api.api('GET', '/api/v3/depth', body)
        sell1 = respond['asks'][0]
        sell2 = respond['asks'][1]
        print(f'\r币本位\tbuy1: {buy1}, buy2: {buy2}  现货\tsell1: {sell1}, sell2: {sell2}', end='')
