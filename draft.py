import asyncio
import websockets
import json


async def connect_to_wss(uri):
    # 连接到WSS服务器
    async with websockets.connect(uri) as websocket:
        # 执行一些操作，例如发送和接收消息
        # data = {}
        # await websocket.send(json.dumps(data))
        while 1:
            response = await websocket.recv()
            buy1 = json.loads(response)['b'][0]
            buy2 = json.loads(response)['b'][1]
            print(f'\rbuy1: {buy1} buy2: {buy2}', end='')


# WSS服务器地址，包含协议
wss_url = "wss://dstream.binance.com/ws/wifusd_perp@depth5"

# 运行异步事件循环
loop = asyncio.get_event_loop()
loop.run_until_complete(connect_to_wss(wss_url))