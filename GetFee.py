from BinanceAPI import BinanceAPI
import matplotlib.pyplot as plt

base_url = 'https://dapi.binance.com'
api_key = 'i7F6rx3Tcz6eJlSVzBc4dpV6qyszCiCOIpSz7gv9mdyq9UjVizrlu2kkmlvUIJSw'
secret_key = 'mwU7KCworFZ17WIOqRuGaRmtwT3nnUDBhtg8HQf9CHFB7KVSxev0Rwym5mgfWjDx'

binance = BinanceAPI(base_url, api_key, secret_key)
symbols = ['WIFUSD_PERP', 'EOSUSD_PERP']

fee_list = []
for symbol in symbols:
    body = {
        'symbol': symbol,
        'limit': 100
    }
    response = binance.IO('GET', '/dapi/v1/fundingRate', body)
    fee_list.append(response)
print(fee_list)
fee_line = {}
for i in range(len(symbols)):
    fee_line[symbols[i]] = list(map(lambda x: float(x['fundingRate']), fee_list[i]))

for symbol, data in fee_line.items():
    plt.plot(data, label=symbol)
plt.legend(loc='best')
plt.show()
