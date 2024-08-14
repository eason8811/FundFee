from BinanceAPI import BinanceAPI
import time

base_url_spot = 'https://api.binance.com'
base_url_coin = 'https://dapi.binance.com'
api_key = 'i7F6rx3Tcz6eJlSVzBc4dpV6qyszCiCOIpSz7gv9mdyq9UjVizrlu2kkmlvUIJSw'
secret_key = 'mwU7KCworFZ17WIOqRuGaRmtwT3nnUDBhtg8HQf9CHFB7KVSxev0Rwym5mgfWjDx'

spot_api = BinanceAPI(base_url_spot, api_key, secret_key)
coin_api = BinanceAPI(base_url_coin, api_key, secret_key)

symbols = ['WIFUSD_PERP']

fund = 1330
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
            if buy_price != 0 and sell_price != 0 and (buy_price - sell_price) / sell_price * 100 > 0.12:
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


# 791.6667    12.0374     11.9453
# 1.68        1.6615      1.6743
#
# 792.61      12.03       11.95
# 1.679       1.663       1.673
#
#
# 1.68*791.6667/(791.6667+12.0374+11.9453)+1.6615*12.0374/(791.6667+12.0374+11.9453)+1.6743*11.9453/(791.6667+12.0374+11.9453)
# 1.6796434986527298
#
# 1.679*792.61/(792.61+12.03+11.95)+1.663*12.03/(792.61+12.03+11.95)+1.673*11.95/(792.61+12.03+11.95)
# 1.6786764839148165
# 实际成交价差：
# 0.0005760578331675402
#
# 现货手续费:   0.1%
# 币本位手续费:  0.05%
# 初始资金： 1370 USDT
#
# 1370    1370*(1-0.001)  1368.63*(1-0.0005)   1367.945685*(1+0.000576)  1368.7337*(1-0.0005)  1368.04933315*(1-0.001)
# 1370 =>    1368.63 =>      1367.945685 =>           1368.7337 =>          1368.04933315 =>     1366.6812838168498
#
# 1366.6812838168498 - 1370 = -3.3187161831501726
# 1368.7337*0.0001 = 0.13687337   一期收入
# 0.13687337 * 3 = 0.41062011     一天收入
# 0.41062011 * 3 = 1.23186033     三天收入
# 3.3187161831501726 / 0.41062011 = 8.0822    需要八天才能回收手续费
