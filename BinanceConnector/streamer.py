import asyncio
import json
import os
from pydoc import cli
import time
from datetime import datetime as dt
from multiprocessing import JoinableQueue as Queue
from threading import Thread
import websockets

class BinanceClient(Thread):

    def __init__(self):

        super(BinanceClient, self).__init__()
        self.queue = Queue()
        self.websocket = None
        self.symbol = None
        self.retry_counter = 0
        self.last_subscribe_time = None

    async def subscribe(self):
        try:
            url = "wss://stream.binance.com:9443/ws"
            subscribe = {
                "method": "SUBSCRIBE",
                "params": ["btcusdt@kline_1m"],
                "id": 1
            }

            socket = await websockets.connect(url)
            print("opened connection")
            msg = json.dumps(subscribe, ensure_ascii=False)
            await asyncio.wait_for(socket.send(msg), timeout=60)
            print("sending")
            while True:
                msg = await socket.recv()
                json_msg = json.loads(msg)
                if 'result' in json_msg:
                    if json_msg['result'] is not None:
                        raise "Unsucessul Connection"
                else:
                    print(json.dumps(json_msg, indent=2))

        except websockets.ConnectionClosed as exception:
            pass

    async def unsubscribe(self):
        pass

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    client = BinanceClient()
    loop.run_until_complete(client.subscribe())
