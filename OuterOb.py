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
            sell1 = respond['asks'][0]
            sell2 = respond['asks'][1]
            body = {
                'symbol': symbol.replace('_PERP', '') + 'T',
                'limit': 5
            }
            respond = spot_api.api('GET', '/api/v3/depth', body)
            buy1 = respond['bids'][0]
            buy2 = respond['bids'][1]

            buy_price = 0
            sell_price = 0
            if float(sell1[1]) * 10 >= fund:
                sell_price = float(sell1[0])
            elif float(sell1[1]) * 10 < fund <= (float(sell1[1]) + float(sell2[1])) * 10:
                sell_price = (float(sell1[0]) * (float(sell1[1]) * 10 / fund)
                              + float(sell2[0]) * ((fund - float(sell1[1]) * 10) / fund))
            if float(buy1[1]) * float(buy1[0]) >= fund:
                buy_price = float(buy1[0])

            print(f'\r币本位\tsell1: {sell1}, sell2: {sell2}  现货\tbuy1: {buy1}, buy2: {buy2}'
                  f'\t{round((buy_price - sell_price) / sell_price * 100, 5) if buy_price != 0 and sell_price != 0 else 0}%',
                  end='')
            count += 0.1
            if count >= 1.0:
                with open('cache.txt', 'a') as f:
                    f.write(f'{(buy_price - sell_price) / sell_price if buy_price != 0 and sell_price != 0 else 0}\n')
                count = 0

                body = {
                    'timestamp': int(time.time() * 1000)
                }
                respond = coin_api.api('GET', '/dapi/v1/account', body)

                margin_info = {}
                position_info = {}
                for margin_info in respond['assets']:
                    if margin_info['asset'] == symbol.replace('USD_PERP', ''):
                        break
                for position_info in respond['positions']:
                    if position_info['symbol'] == symbol and position_info['positionSide'] == 'SHORT':
                        break

                total_value = float(margin_info["marginBalance"]) * buy_price
                print(f'\n钱包总额: {margin_info["marginBalance"]}\t仓位数量: {position_info["notionalValue"]}\t'
                      f'差值:{float(margin_info["marginBalance"]) + float(position_info["notionalValue"])}'
                      f'\t总价值: {total_value}')


    except Exception as e:
        print(f'\n出现错误：{type(e)} : {e}\n时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n')
