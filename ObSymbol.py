from BinanceAPI import BinanceAPI
import time

base_url_spot = 'https://api.binance.com'
base_url_coin = 'https://dapi.binance.com'
api_key = 'i7F6rx3Tcz6eJlSVzBc4dpV6qyszCiCOIpSz7gv9mdyq9UjVizrlu2kkmlvUIJSw'
secret_key = 'mwU7KCworFZ17WIOqRuGaRmtwT3nnUDBhtg8HQf9CHFB7KVSxev0Rwym5mgfWjDx'

spot_api = BinanceAPI(base_url_spot, api_key, secret_key)
coin_api = BinanceAPI(base_url_coin, api_key, secret_key)

symbols = ['WIFUSD_PERP']

fund = 20
count = 0

while True:
    try:
        time.sleep(0.2)
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

            buy_price = 0
            sell_price = 0
            if float(buy1[1]) * 10 >= fund:
                buy_price = float(buy1[0])
            elif float(buy1[1]) * 10 < fund <= (float(buy1[1]) + float(buy2[1])) * 10:
                buy_price = (float(buy1[0]) * (float(buy1[1]) * 10 / fund)
                             + float(buy2[0]) * ((fund - float(buy1[1]) * 10) / fund))
            if float(sell1[1]) * float(sell1[0]) >= fund:
                sell_price = float(sell1[0])
            if buy_price != 0 and sell_price != 0 and (buy_price - sell_price) / sell_price * 100 > 0.1:
                print(f'\n\n有机会！{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
                print(f'币本位\tbuy1: {buy1}, buy2: {buy2}  现货\tsell1: {sell1}, sell2: {sell2}'
                      f'\t{(buy_price - sell_price) / sell_price * 100 if buy_price != 0 and sell_price != 0 else 0}%')
                print(f'买价: {sell_price}, 卖价: {buy_price}\n')

                body = {
                    'symbol': symbol.replace('_PERP', 'T'),
                    'side': 'BUY',
                    'type': 'MARKET',
                    'quantity': round(fund / sell_price, 2),
                    'newOrderRespType': 'RESULT',
                    'timestamp': int(time.mktime(time.localtime())) * 1000,
                }
                response = spot_api.api('POST', '/api/v3/order', body)
                print(response)
                buy_spot_order_id = response['orderId']
                real_buy_quantity = float(response['executedQty']) * (1 - 0.001)

                while True:
                    body = {
                        'type': 'MAIN_CMFUTURE',
                        'asset': symbol.replace('USD_PERP', ''),
                        'amount': real_buy_quantity,
                        'timestamp': int(time.mktime(time.localtime())) * 1000,
                    }

                    response = spot_api.api('POST', '/sapi/v1/asset/transfer', body)
                    print(response)
                    if response.get('tranId') is not None:
                        break

                body = {
                    'symbol': symbol,
                    'side': 'SELL',
                    'positionSide': 'SHORT',
                    'type': 'MARKET',
                    'quantity': int(round(real_buy_quantity * sell_price / 10, 0)),
                    'timestamp': int(time.mktime(time.localtime())) * 1000,
                }

                response = coin_api.api('POST', '/dapi/v1/order', body)
                print(response)
                sell_coin_order_id = response['orderId']

                body = {
                    'symbol': symbol.replace('_PERP', 'T'),
                    'orderId': buy_spot_order_id,
                    'timestamp': int(time.mktime(time.localtime())) * 1000,
                }
                response = spot_api.api('GET', '/api/v3/order', body)
                buy_spot_price = float(response['cummulativeQuoteQty']) / float(response['executedQty'])

                body = {
                    'symbol': symbol,
                    'orderId': sell_coin_order_id,
                    'timestamp': int(time.mktime(time.localtime())) * 1000,
                }
                response = coin_api.api('GET', '/dapi/v1/order', body)
                sell_coin_price = float(response['avgPrice'])

                print(f'实际成交价差：{round((sell_coin_price - buy_spot_price) / buy_spot_price * 100, 4)}%')
                break

            print(f'\r币本位\tbuy1: {buy1}, buy2: {buy2}  现货\tsell1: {sell1}, sell2: {sell2}'
                  f'\t{(buy_price - sell_price) / sell_price * 100 if buy_price != 0 and sell_price != 0 else 0}%',
                  end='')
            count += 0.1
            if count >= 1.0:
                with open('cache.txt', 'a') as f:
                    f.write(f'{(buy_price - sell_price) / sell_price if buy_price != 0 and sell_price != 0 else 0}\n')
                count = 0
    except Exception as e:
        print(f'\n出现错误：{type(e)} : {e}\n时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n')
