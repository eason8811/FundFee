from BinanceAPI import BinanceAPI
import time

base_url_coin = 'https://dapi.binance.com'
api_key = 'i7F6rx3Tcz6eJlSVzBc4dpV6qyszCiCOIpSz7gv9mdyq9UjVizrlu2kkmlvUIJSw'
secret_key = 'mwU7KCworFZ17WIOqRuGaRmtwT3nnUDBhtg8HQf9CHFB7KVSxev0Rwym5mgfWjDx'

coin_api = BinanceAPI(base_url_coin, api_key, secret_key)
symbols = ['WIFUSD_PERP']

for symbol in symbols:
    body = {
        'symbol': symbol,
        'incomeType': 'FUNDING_FEE',
        'startTime': int(time.mktime(time.strptime('2024-08-14 0:0:0', '%Y-%m-%d %H:%M:%S'))) * 1000,
        'endTime': int(time.time()) * 1000,
        'timestamp': int(time.time()) * 1000,
    }
    respond = coin_api.api('GET', '/dapi/v1/income', body)

    fund_fee_list = []
    for item in respond:
        fund_fee_list.append(float(item['income']))

    print(fund_fee_list)
    print(f'总额为 {round(sum(fund_fee_list), 9)}')

    body = {
        'symbol': symbol,
    }
    respond = coin_api.api('GET', '/dapi/v1/ticker/price', body)
    now_price = float(respond[0]['price'])
    print(f'当前价格为 {now_price}')
    print(f'净收益为 {round(sum(fund_fee_list) * now_price, 9)}')
